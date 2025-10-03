# HIT137 Assignment 3 — Tkinter AI GUI (Local Models)

Runs locally on CPU using Hugging Face `transformers` + `torch`.  
Models:

- Text Summarization: `facebook/bart-large-cnn`
- Text Generation: `openai-community/gpt2`
- Translation (EN → target): `Helsinki-NLP/opus-mt-*` (French, German, Spanish, Italian, Russian, Chinese, Japanese, Arabic, Nepali, Hindi)
- Image Classification: `google/vit-base-patch16-224`

## Setup

```bash
python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install -r requirements.txt


or
# Install these packages
pip install customtkinter
pip install Pillow
pip install transformers
pip install torch
pip install sentencepiece
pip install sacremoses
pip install tokenizers
pip install datasets
pip install tqdm
pip install packaging

```

## Run

```bash
python3 main.py
```

## OOP Concepts Used

- Encapsulation: `BaseModelAdapter` hides private pipeline (`__pipeline`)
- Inheritance: adapters inherit from `BaseModelAdapter`
- Multiple Inheritance: adapters mix in `SaveOutputMixin`; GUI mixes `ThemingMixin`
- Polymorphism: common `.run(raw_input)` across adapters
- Method Overriding: `preprocess` / `postprocess` per adapter
- Multiple Decorators: `@log_action` + `@measure_time` on GUI handlers
