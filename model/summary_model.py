# summary_model.py

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from model.base_model import BaseNLPModel
from Utils.decorators import log_action, measure_time

class Summarizer(BaseNLPModel):
    """Summarization model (BART)."""

    def __init__(self, model_name: str = "facebook/bart-large-cnn"):
        super().__init__(model_name)   # inheritance
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    @log_action
    @measure_time
    def run(self, text: str, max_length: int = 150, min_length: int = 40) -> str:
        """Override base method: run() → summarization."""
        inputs = self.tokenizer([text], return_tensors="pt", max_length=1024, truncation=True)
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                min_length=min_length,
                length_penalty=2.0,
                num_beams=4,
                early_stopping=True
            )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
