from abc import ABC, abstractmethod

class BaseNLPModel(ABC):
    """Abstract base class for NLP models."""

    def __init__(self, model_name: str):
        self._model_name = model_name   # encapsulation: private attribute

    @abstractmethod
    def run(self, text: str, **kwargs) -> str:
        """Run inference on input text."""
        pass

    def get_model_name(self):
        """Accessor for encapsulated attribute."""
        return self._model_name
