# HIT137 Assignment 3 — Tkinter AI GUI (Local Models)

Runs locally on CPU using Hugging Face `transformers` + `torch`.
Models:
- Text Classification: `distilbert-base-uncased-finetuned-sst-2-english`
- Image Classification: `google/vit-base-patch16-224`

## Setup
```bash
python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install -r requirements.txt
```

## Run
```bash
python3 app.py
```

## OOP Concepts Used
- Encapsulation: `BaseModelAdapter` hides private pipeline (`__pipeline`)
- Inheritance: adapters inherit from `BaseModelAdapter`
- Multiple Inheritance: adapters mix in `SaveOutputMixin`; GUI mixes `ThemingMixin`
- Polymorphism: common `.run(raw_input)` across adapters
- Method Overriding: `preprocess` / `postprocess` per adapter
- Multiple Decorators: `@log_action` + `@measure_time` on GUI handlers
