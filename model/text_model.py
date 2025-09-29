# text_model.py

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from model.base_model import BaseNLPModel
from Utils.decorators import log_action, measure_time

class TextGenerator(BaseNLPModel):
    """Text generation model (GPT-2)."""

    def __init__(self, model_name: str = "openai-community/gpt2"):
        super().__init__(model_name)   # inheritance
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

    @log_action
    @measure_time
    def run(self, text: str, max_length: int = 150, temperature: float = 0.7, top_p: float = 0.9) -> str:
        """Override base method: run() → text generation."""
        inputs = self.tokenizer(text, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                temperature=temperature,
                top_p=top_p,
                do_sample=True
            )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
    ...
    def get_model_name(self):
        return "GPT-2 Text Generator"