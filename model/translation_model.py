# translation_model.py

from transformers import pipeline


class TranslationModelAdapter:
    """
    Adapter for Hugging Face translation models (English → target language).
    """

    SUPPORTED_MODELS = {
       
        "French": "Helsinki-NLP/opus-mt-en-fr",
        "German": "Helsinki-NLP/opus-mt-en-de",
        "Spanish": "Helsinki-NLP/opus-mt-en-es",
        "Italian": "Helsinki-NLP/opus-mt-en-it",
        "Russian": "Helsinki-NLP/opus-mt-en-ru",
        "Chinese": "Helsinki-NLP/opus-mt-en-zh",   
        "Japanese": "Helsinki-NLP/opus-mt-en-jap",  
        "Arabic": "Helsinki-NLP/opus-mt-en-ar",
        "Nepali": "Helsinki-NLP/opus-mt-en-ne",    # may fail
        "Hindi": "Helsinki-NLP/opus-mt-en-hi",    
}


    def __init__(self, target_lang: str = "French"):
        """
        Initialize translation model for the given target language (default: EN → FR).
        """
        self.target_lang = target_lang
        self.model_name = self.SUPPORTED_MODELS.get(
            target_lang, "Helsinki-NLP/opus-mt-en-fr"
        )
        try:
            self.pipeline = pipeline("translation", model=self.model_name)
        except Exception as e:
            raise RuntimeError(
                f"Failed to load model {self.model_name}. "
                f"Make sure 'sentencepiece' is installed for opus-mt models."
            ) from e

    def run(self, text: str) -> str:
        """Translate text to the target language."""
        result = self.pipeline(text, max_length=200)
        return result[0]["translation_text"]

    def save_output(self, result: str):
        """
        Save translations into per-language files under ./outputs.
        Example path: outputs/translation_french.txt
        """
        import os
        os.makedirs("outputs", exist_ok=True)
        lang_file = f"outputs/translation_{self.target_lang.lower()}.txt"
        try:
            with open(lang_file, "a", encoding="utf-8") as f:
                f.write(result + "\n")
            return lang_file
        except Exception as e:
            print(f"Could not save output: {e}")
            return None

    # Friendly name for UI / model selector
    def get_model_name(self) -> str:
        return f"EN→{self.target_lang} Translator"

    def __str__(self) -> str:
        return self.get_model_name()
