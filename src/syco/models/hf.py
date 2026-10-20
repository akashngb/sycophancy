"""Hugging Face Transformers backend.

Loads any chat-tuned model with transformers, uses the tokenizer's chat
template, auto-selects cuda/mps/cpu, and defaults to greedy decoding.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from syco.models.base import Message
from syco.utils.device import pick_device


@dataclass
class HFBackend:
    model_id: str
    name: str = "hf"
    device: str | None = None  # None -> auto
    dtype: str = "auto"  # "auto", "float16", "bfloat16", "float32"
    trust_remote_code: bool = False
    _loaded: bool = field(default=False, init=False, repr=False)
    _model: Any = field(default=None, init=False, repr=False)
    _tokenizer: Any = field(default=None, init=False, repr=False)
    _resolved_device: str = field(default="cpu", init=False, repr=False)

    def _load(self) -> None:
        if self._loaded:
            return
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        self._resolved_device = pick_device(self.device)

        if self.dtype == "auto":
            # On CPU, float32 is safest and fastest for small models.
            # On MPS, float16 can be flaky for some ops; prefer float32.
            # On CUDA, bfloat16 if supported, otherwise float16.
            if self._resolved_device == "cuda":
                torch_dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
            else:
                torch_dtype = torch.float32
        else:
            torch_dtype = getattr(torch, self.dtype)

        self._tokenizer = AutoTokenizer.from_pretrained(
            self.model_id, trust_remote_code=self.trust_remote_code
        )
        if self._tokenizer.pad_token_id is None:
            self._tokenizer.pad_token = self._tokenizer.eos_token

        self._model = AutoModelForCausalLM.from_pretrained(
            self.model_id,
            torch_dtype=torch_dtype,
            trust_remote_code=self.trust_remote_code,
        )
        self._model.to(self._resolved_device)
        self._model.eval()
        self._loaded = True

    def generate(self, messages: list[Message], **params: Any) -> str:
        import torch

        self._load()
        max_new_tokens = int(params.get("max_new_tokens", 128))
        temperature = float(params.get("temperature", 0.0))
        top_p = float(params.get("top_p", 1.0))
        do_sample = temperature > 0.0

        prompt = self._tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        inputs = self._tokenizer(prompt, return_tensors="pt").to(self._resolved_device)

        with torch.no_grad():
            out = self._model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=do_sample,
                temperature=temperature if do_sample else 1.0,
                top_p=top_p if do_sample else 1.0,
                pad_token_id=self._tokenizer.pad_token_id,
            )
        gen = out[0, inputs["input_ids"].shape[1] :]
        text = self._tokenizer.decode(gen, skip_special_tokens=True)
        return text.strip()

    def hidden_states(self, messages: list[Message], layers: list[int] | None = None) -> dict:
        """Return hidden states for the final prompt token.

        Useful for interpretability experiments (probes, steering).
        Returns a dict with keys: "layers" (list[int]) and "activations"
        (list[torch.Tensor] of shape [hidden_size]).
        """
        import torch

        self._load()
        prompt = self._tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        inputs = self._tokenizer(prompt, return_tensors="pt").to(self._resolved_device)
        with torch.no_grad():
            out = self._model(**inputs, output_hidden_states=True)
        all_hidden = out.hidden_states  # tuple: (num_layers + 1, batch, seq, hidden)
        if layers is None:
            layers = list(range(len(all_hidden)))
        acts = [all_hidden[i][0, -1, :].detach().cpu() for i in layers]
        return {"layers": layers, "activations": acts}

    def info(self) -> dict[str, Any]:
        return {
            "backend": self.name,
            "model_id": self.model_id,
            "device": self._resolved_device if self._loaded else self.device or "auto",
            "dtype": self.dtype,
        }
