# image_model.py

import os
from transformers import pipeline
from model.base_model import BaseModelAdapter


class ImageClassificationModelAdapter(BaseModelAdapter):
    """
    Adapter for image classification using ViT.
    Your BaseModelAdapter sets (model_name, task) and may implement shared utilities.
    """

    def __init__(self):
        super().__init__(
            model_name="google/vit-base-patch16-224", task="image-classification"
        )

    def _build_pipeline(self):
        # Lazily build a HF pipeline for image classification
        return pipeline(self.task, model=self.model_name)

    def preprocess(self, raw_input: str):
        # Here, input is just an image path selected via filedialog
        return raw_input

    def postprocess(self, output):
        # Format top-3 predictions nicely
        return "\n".join([f"{o['label']} ({o['score']:.2f})" for o in output[:3]])

    def save_output(self, result: str, filename: str = "image_output.txt"):
        os.makedirs("outputs", exist_ok=True)
        path = os.path.join("outputs", filename)
        with open(path, "a", encoding="utf-8") as f:
            f.write(result + "\n")
        return path

    # Friendly name for UI
    def get_model_name(self) -> str:
        return "ViT Image Classifier"

    def __str__(self) -> str:
        return self.get_model_name()
