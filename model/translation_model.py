from transformers import pipeline


class TranslationModelAdapter:
    """
    Adapter for Hugging Face translation models.
    Supports multiple target languages (English → X).
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
        "Nepali": "Helsinki-NLP/opus-mt-en-ne",
        "Hindi": "Helsinki-NLP/opus-mt-en-hi",
    }

    def __init__(self, target_lang: str = "French"):
        """
        Initialize translation model for a given target language.
        Defaults to English → French.
        """
        self.target_lang = target_lang
        model_name = self.SUPPORTED_MODELS.get(
            target_lang, "Helsinki-NLP/opus-mt-en-fr"
        )
        try:
            self.pipeline = pipeline("translation", model=model_name)
        except Exception as e:
            raise RuntimeError(
                f"Failed to load model {model_name}. Make sure 'sentencepiece' is installed."
            ) from e

    def run(self, text: str) -> str:
        """
        Translate the given text to the target language.
        """
        result = self.pipeline(text, max_length=200)
        return result[0]["translation_text"]

    def save_output(self, result: str):
        """
        Save translations into per-language files.
        Example: translation_french.txt
        """
        lang_file = f"translation_{self.target_lang.lower()}.txt"
        try:
            with open(lang_file, "a", encoding="utf-8") as f:
                f.write(result + "\n")
        except Exception as e:
            print(f"Could not save output: {e}")
