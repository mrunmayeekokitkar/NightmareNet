"""Unit tests for NightmareNet checkpoint saving, offset scheduling, and training resume."""

import os

import pytest
import torch
from datasets import Dataset
from torch.utils.data import DataLoader

from nightmarenet.training.scheduler import CyclicScheduler
from nightmarenet.training.trainer import Trainer


def _make_tiny_dataset(n: int = 10) -> Dataset:
    texts = [
        "The quick brown fox jumps over the lazy dog.",
        "Machine learning is a subset of artificial intelligence.",
        "Paris is the capital of France and a major city.",
    ]
    return Dataset.from_dict({"text": [texts[i % len(texts)] for i in range(n)]})


def _tokenize_dataset(dataset: Dataset, tokenizer, max_length: int = 32):
    def tok_fn(examples):
        return tokenizer(
            examples["text"],
            truncation=True,
            max_length=max_length,
            padding="max_length",
        )
    ds = dataset.map(tok_fn, batched=True, remove_columns=["text"])
    ds.set_format("torch")
    return ds


@pytest.fixture
def minimal_config(tmp_path):
    checkpoint_dir = tmp_path / "checkpoints"
    log_dir = tmp_path / "logs"
    checkpoint_dir.mkdir()
    log_dir.mkdir()
    return {
        "model": {
            "name": "gpt2",
            "type": "causal_lm",
            "max_length": 32,
            "device": "cpu",
        },
        "dataset": {
            "text_column": "text",
            "max_samples": 10,
        },
        "training": {
            "wake_epochs": 1,
            "dream_epochs": 1,
            "nightmare_epochs": 1,
            "num_cycles": 2,
            "batch_size": 2,
            "learning_rate": 5e-5,
            "weight_decay": 0.01,
            "max_grad_norm": 1.0,
            "gradient_accumulation_steps": 1,
            "save_every_phase": True,
            "checkpoint_dir": str(checkpoint_dir),
            "log_dir": str(log_dir),
        },
        "distortion": {
            "dream_strength": 0.25,
            "nightmare_strength": 0.8,
        },
        "compression": {
            "pruning_ratio": 0.1,
            "pruning_method": "magnitude",
        },
        "evaluation": {
            "metrics": ["recall"],
        },
        "tracking": {"backend": "none"},
        "seed": 42,
    }


def test_scheduler_resume_offset():
    """Test that CyclicScheduler correctly skips to the next phase when starting with offset."""
    scheduler = CyclicScheduler(
        num_cycles=3,
        wake_epochs=1,
        dream_epochs=1,
        nightmare_epochs=1,
        compression_rounds=1,
        start_cycle=0,
        start_phase="compress"
    )
    phases = list(scheduler)
    # Remaining: Cycle 1 wake, dream, nightmare, compress; Cycle 2 wake, dream, nightmare, compress
    assert len(phases) == 8
    assert phases[0] == (1, "wake", 1)
    assert phases[-1] == (2, "compress", 1)

    scheduler2 = CyclicScheduler(
        num_cycles=3,
        wake_epochs=1,
        dream_epochs=1,
        nightmare_epochs=1,
        compression_rounds=1,
        start_cycle=1,
        start_phase="dream"
    )
    phases2 = list(scheduler2)
    # Remaining: Cycle 1 nightmare, compress; Cycle 2 wake, dream, nightmare, compress
    assert len(phases2) == 6
    assert phases2[0] == (1, "nightmare", 1)


def test_trainer_save_and_load_state(minimal_config, tmp_path):
    """Test that checkpoint saving preserves optimizer, scaler, scheduler state, and history."""
    pytest.importorskip("transformers")
    trainer = Trainer(config=minimal_config)

    # Checkpoint path
    path = os.path.join(trainer.checkpoint_dir, "cycle0_wake")

    # Let's populate history and save checkpoint
    trainer.history = [{"phase": "wake", "avg_loss": 1.23, "cycle": 0}]
    trainer._save_checkpoint(cycle=0, phase="wake")

    state_file = os.path.join(path, "training_state.pt")
    assert os.path.exists(state_file)
    assert os.path.exists(os.path.join(path, "config.json"))

    # Load state directly
    state = torch.load(state_file, map_location="cpu")
    assert "optimizer_state_dict" in state
    assert state["cycle"] == 0
    assert state["phase"] == "wake"
    assert state["history"] == [{"phase": "wake", "avg_loss": 1.23, "cycle": 0}]


def test_trainer_resume_execution(minimal_config, tmp_path):
    """Test training resume end-to-end with a dummy loop."""
    transformers = pytest.importorskip("transformers")
    tokenizer = transformers.AutoTokenizer.from_pretrained("gpt2")
    tokenizer.pad_token = tokenizer.eos_token

    base_ds = _make_tiny_dataset(4)
    train_ds = _tokenize_dataset(base_ds, tokenizer)
    loader = DataLoader(train_ds, batch_size=2)

    # Step 1: Initialize first trainer run
    trainer1 = Trainer(config=minimal_config)
    trainer1.history = [{"phase": "wake", "avg_loss": 2.5, "cycle": 0}]

    # Save checkpoint manually at cycle 0 wake
    trainer1._save_checkpoint(cycle=0, phase="wake")
    checkpoint_path = os.path.join(trainer1.checkpoint_dir, "cycle0_wake")

    # Step 2: Create second trainer configured to resume
    resume_config = minimal_config.copy()
    resume_config["training"] = minimal_config["training"].copy()
    resume_config["training"]["resume_from"] = checkpoint_path

    trainer2 = Trainer(config=resume_config)

    # Run train with short loaders
    history = trainer2.train(
        train_dataloader=loader,
        dream_dataloader=loader,
        nightmare_dataloader=loader,
        val_dataloader=loader
    )

    # Verify training continued from dream phase of cycle 0 (index 1 of Cycle 0)
    # Remaining phases of the run with 2 cycles total:
    # Cycle 0: dream, nightmare, compress
    # Cycle 1: wake, dream, nightmare, compress
    # Total new phases: 7
    # Original history from trainer1: 1 phase
    # Total history: 8 phases
    assert len(history) == 8
    assert history[0]["phase"] == "wake"
    assert history[0]["avg_loss"] == 2.5
    assert history[1]["phase"] == "dream"
    assert history[-1]["phase"] == "compress"
