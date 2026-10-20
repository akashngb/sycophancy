# Setup guide

If something goes wrong, check the troubleshooting section at the end
before asking in Discord.

## Install uv

uv is a fast Python package and project manager. We use it for the venv,
dependency resolution, and running commands.

- **macOS and Linux**:
  `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Windows**:
  `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`

Verify: `uv --version`.

## Clone and install

```bash
git clone https://github.com/akashngb/sycophancy.git
cd sycophancy
uv sync --extra dev
```

The first `uv sync` downloads torch, transformers, and friends. Expect
a few hundred MB of disk and a couple of minutes.

Copy the env file. The starter run does not need any keys.

```bash
cp .env.example .env
```

## First run

Confirm the fake backend works end to end. No model download, no GPU.

```bash
uv run syco run --config configs/experiments/flip_rate_fake.yaml
```

Then try the tiny model (about 1 GB download the first time).

```bash
make demo
```

## macOS, Apple Silicon

- Everything should "just work". The HF backend auto-selects MPS.
- If you see MPS numeric errors on specific operators, set
  `SYCO_DEVICE=cpu` in `.env` and rerun.
- `vllm` is not supported on macOS. Use the HF backend or Ollama.

## Windows

- Install uv via PowerShell (see above).
- Prefer Windows Terminal + PowerShell 7 or WSL2.
- CPU-only works. CUDA works if you have an NVIDIA GPU and a matching
  driver. Install the CUDA-enabled torch build before `uv sync --extra dev`
  by adding `--extra-index-url https://download.pytorch.org/whl/cu121`.
- Long paths: enable `LongPathsEnabled` if you hit "path too long" errors.

## Linux

- CPU-only works. CUDA works with a matching NVIDIA driver.
- `vllm` is supported on Linux with CUDA. Install with
  `uv sync --extra serve`.

## Optional: Ollama (local server)

Ollama is a nice way to run small quantized models on a laptop.

1. Install from https://ollama.com .
2. Pull a model: `ollama pull qwen2.5:0.5b-instruct`.
3. Edit `configs/models/example_ollama.yaml`:
   change `backend: fake` to `backend: ollama` and uncomment the
   `model_id` line.
4. Point an experiment config at it.

## Optional: LM Studio or vLLM (OpenAI-compatible server)

If you are running an OpenAI-compatible server locally (LM Studio, vLLM,
llama.cpp with the OpenAI shim), set `OPENAI_COMPATIBLE_BASE_URL` in
`.env` (default is `http://localhost:8000/v1`) and use a model config
with `backend: openai_compat`.

## Hugging Face login (for gated models)

Some models like Llama 3 and Gemma are gated. You need to accept the
license on the model's HF page, then put a token in `.env`:

```bash
HF_TOKEN=hf_...
```

transformers reads this automatically. You can also run
`uv run huggingface-cli login` if you prefer the credential file.

## Common errors

- `OSError: ... not a local folder and is not a valid model identifier`:
  check the model id in your YAML. If it is gated, you need `HF_TOKEN`.
- `ValueError: BackendCompilerFailed` on MPS: set `SYCO_DEVICE=cpu`.
- `torch` fails to import on Windows: your CPU may be missing AVX2.
  Install an older torch build or run on a different machine.
- "Permission denied" when running `run.sh`: `chmod +x <path>`.
- Out of RAM with a 7B model on CPU: use the tiny or small model, or
  rent a GPU. See `docs/experiments-menu.md`.
- First `make demo` is slow: it is downloading the model. Later runs
  are fast.
