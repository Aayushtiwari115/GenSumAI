import os
from .base import BaseModelAdapter
from transformers import pipeline

class ImageClassificationModelAdapter(BaseModelAdapter):
    def __init__(self):
        super().__init__(model_name="google/vit-base-patch16-224", task="image-classification")

    def _build_pipeline(self):
        return pipeline(self.task, model=self.model_name)

    def preprocess(self, raw_input: str):
        return raw_input  # here, it’s just the image path

    def postprocess(self, output):
        # Show top-3 predictions nicely
        return "\n".join([f"{o['label']} ({o['score']:.2f})" for o in output[:3]])
    def save_output(self, result: str, filename: str = "translation_output.txt"):
        os.makedirs("outputs", exist_ok=True)
        path = os.path.join("outputs", filename)
        with open(path, "a", encoding="utf-8") as f:
            f.write(result + "\n")
        return path