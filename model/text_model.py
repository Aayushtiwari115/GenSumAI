# text_model.py

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from model.base_model import BaseNLPModel
from Utils.decorators import log_action, measure_time


class TextGenerator(BaseNLPModel):
    """Text generation model (GPT-2)."""

    def __init__(self, model_name: str = "openai-community/gpt2"):
        super().__init__(model_name)   # inheritance stores self.model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        # GPT-2 has no pad token; map pad→eos to avoid warnings when sampling
        if self.tokenizer.pad_token_id is None:
            self.tokenizer.pad_token_id = self.tokenizer.eos_token_id
        self.model.eval()

    @log_action
    @measure_time
    def run(
        self,
        text: str,
        max_length: int = 150,
        temperature: float = 0.7,
        top_p: float = 0.9,
    ) -> str:
        """Override base method: run() → text generation."""
        inputs = self.tokenizer(text, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                temperature=temperature,
                top_p=top_p,
                do_sample=True,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
            )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Friendly name for UI
    def get_model_name(self) -> str:
        return "GPT-2 Text Generator"

    def __str__(self) -> str:
        return self.get_model_name()
