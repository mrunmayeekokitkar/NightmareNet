"""Tests for Optuna Hyperparameter Optimization integration."""

import os
import tempfile
from unittest import mock

import pytest
import yaml

try:
    import optuna

    from nightmarenet.optimization.hpo import OPTUNA_AVAILABLE, HyperparameterOptimizer
except ImportError:
    OPTUNA_AVAILABLE = False


@pytest.fixture
def hpo_config_path():
    config = {
        "model": {"name": "gpt2"},
        "hpo": {
            "study_name": "test-study",
            "storage": "sqlite:///:memory:",
            "direction": "maximize",
            "n_trials": 2,
            "pruning": True,
            "search_space": {
                "training.learning_rate": {
                    "type": "float",
                    "low": 1e-5,
                    "high": 1e-3,
                    "log": True,
                },
                "training.batch_size": {
                    "type": "categorical",
                    "choices": [4, 8],
                },
            },
        },
    }
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(config, f)
        path = f.name
    yield path
    os.remove(path)


@pytest.mark.skipif(not OPTUNA_AVAILABLE, reason="Optuna not installed")
@mock.patch("nightmarenet.optimization.hpo.Pipeline")
def test_hyperparameter_optimizer_runs(mock_pipeline_cls, hpo_config_path):
    mock_pipeline = mock.Mock()
    mock_context = mock.Mock()
    mock_context.cancelled = False
    mock_pipeline._context = mock_context
    mock_pipeline_cls.return_value = mock_pipeline

    mock_pipeline.run.return_value = {"robustness_delta": 0.15}

    optimizer = HyperparameterOptimizer(hpo_config_path)
    study = optimizer.optimize()

    assert len(study.trials) == 2
    assert study.best_value == 0.15
    assert mock_pipeline.run.call_count == 2

    call_args = mock_pipeline_cls.call_args_list[0][1]
    trial_config = call_args["config"]
    assert "learning_rate" in trial_config["training"]
    assert "batch_size" in trial_config["training"]
    assert trial_config["training"]["batch_size"] in [4, 8]


@pytest.mark.skipif(not OPTUNA_AVAILABLE, reason="Optuna not installed")
@mock.patch("nightmarenet.optimization.hpo.Pipeline")
def test_hyperparameter_optimizer_pruning(mock_pipeline_cls, hpo_config_path):
    mock_pipeline = mock.Mock()
    mock_context = mock.Mock()
    mock_context.cancelled = False
    mock_pipeline._context = mock_context

    def cancel():
        mock_context.cancelled = True

    mock_pipeline.cancel = mock.Mock(side_effect=cancel)

    def side_effect_run():
        on_event = mock_pipeline_cls.call_args[1]["on_event"]
        metrics = {"status": "training", "current_cycle": 1, "phase_loss": 10.0}
        on_event(metrics)
        return {"robustness_delta": 0.05}

    mock_pipeline.run.side_effect = side_effect_run
    mock_pipeline_cls.return_value = mock_pipeline

    optimizer = HyperparameterOptimizer(hpo_config_path)

    with mock.patch("optuna.Trial.should_prune", return_value=True):
        study = optimizer.optimize()

    for trial in study.trials:
        assert trial.state == optuna.trial.TrialState.PRUNED
    assert mock_pipeline.cancel.called
