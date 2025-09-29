# base_model.py

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
    

class BaseModelAdapter(ABC):
    def __init__(self, model_name: str, task: str):
        self._model_name = model_name
        self._task = task
        self.__pipeline = None  # private (encapsulation)

    @property
    def model_name(self): return self._model_name
    @property
    def task(self): return self._task

    def _ensure_pipeline(self):
        if self.__pipeline is None:
            self.__pipeline = self._build_pipeline()
        return self.__pipeline

    @abstractmethod
    def _build_pipeline(self): ...
    @abstractmethod
    def preprocess(self, raw_input): ...
    @abstractmethod
    def postprocess(self, raw_output): ...

    def run(self, raw_input):
        x = self.preprocess(raw_input)     # overridden in child
        pipe = self._ensure_pipeline()
        out = pipe(x)
        return self.postprocess(out)       # overridden in child

