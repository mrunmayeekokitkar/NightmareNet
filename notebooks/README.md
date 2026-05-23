# Notebooks

Colab-ready workflows (open in Google Colab from repo):

1. **Quickstart** — distort text + robustness API (`docs/research/benchmark-v1.md` for training)
2. **Benchmark reproduction** — SST-2 with `configs/benchmark_sst2.yaml`
3. **Custom distortions** — register plugins via `nightmarenet.distortions.registry`

```bash
pip install -e ".[dev,api]"
jupyter notebook  # optional local run
```
