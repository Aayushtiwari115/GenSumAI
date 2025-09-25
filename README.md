# HuggingFace_Assessment3

GenSumAI — README

GenSumAI — A modern desktop GUI for lightweight NLP tasks (text generation, summarization) built with customtkinter. GenSumAI wraps simple model adapters (Hugging Face pipeline if available; safe fallbacks otherwise), provides a modern 2025-style UI, non-blocking model runs, a draggable Compose/Results sash, a files viewer, and productivity UX features (keyboard shortcuts, tooltips, activity history).

Table of contents

Features

Requirements & Dependencies

Quick install (macOS / Linux / Windows)

Project layout

How to run

Usage & keyboard shortcuts

Development notes & architecture

Troubleshooting (common errors & fixes)

Assets, fonts & theming

Tests & manual checks

Contributing

License

Features

Modern, clean UI (2025-inspired look)

Two tasks: Text Generation and Summarization

Two-way sync: selecting a task updates the model selector, and vice versa

Non-blocking model runs using a background thread (concurrent.futures.ThreadPoolExecutor)

Draggable input/output sash (resizable Compose and Results areas)

Toggleable Compose (input) area (collapse/expand)

Files & Menu window: browse assets and project files; open text files in a separate window

Compact Activity / History panel

Top navigation with Files/Menu (left), title + model selector (center), Dark Mode + Run (right)

Tooltips, keyboard shortcuts and polished micro-interactions

Graceful fallback if transformers or Pillow are not installed

Requirements & Dependencies

Python 3.9+

pip (or poetry)

(Optional) virtualenv / venv

Python packages:

customtkinter

Pillow (optional — for icons)

transformers (optional — for real model backends)

torch / flax (optional — depending on model backend)

Install minimal packages:

python3 -m venv .venv
source .venv/bin/activate # macOS / Linux

# .venv\Scripts\activate # Windows PowerShell

pip install --upgrade pip
pip install customtkinter
pip install pillow # optional for icons

# Optional: transformers + torch

# pip install transformers torch

Note: transformers + torch are large; only install if required. GenSumAI will run with fallbacks when they are absent.

Quick install (macOS example)
cd /path/to/GenSumAI
python3 -m venv .venv
source .venv/bin/activate
pip install customtkinter pillow
python3 main.py

Project layout
GenSumAI/
├─ main.py
├─ README.md
├─ gui/
│ ├─ **init**.py
│ ├─ app.py
│ ├─ layout.py
│ ├─ theme.py
│ ├─ icons.py
│ └─ assets/ # icon PNGs/SVGs (logo.png, files.png, run.png, etc.)
├─ model/
│ ├─ **init**.py
│ ├─ base_model.py
│ ├─ text_model.py
│ └─ summary_model.py
├─ utils/
│ ├─ **init**.py
│ └─ utils.py # decorators: log_action, measure_time
└─ .venv/

How to run

From the project root (where main.py lives):

python3 main.py

If using a full path to python (as in your earlier logs), run it from the project root so relative imports work:

/usr/local/bin/python3 main.py

Usage & keyboard shortcuts

Run: Ctrl + R

Clear input & output: Ctrl + L

Copy output: Ctrl + C

Toggle Compose (input) area: Ctrl + T

Quit: Ctrl + Q

Top-left: Files / Menu — separate window
Top-center: Title + model selector (model ↔ task sync)
Top-right: Dark mode toggle + Run button

Development notes & architecture

model/\* contains wrappers that implement get_model_name() and run(...). They attempt to use HF pipelines if transformers is installed; otherwise, they return safe fallbacks.

gui/ contains UI split into app.py (application logic), layout.py (UI structure), theme.py (design tokens & colors) and icons.py (image loader).

utils/utils.py provides logging/time decorators consumed by models.

Background inference uses ThreadPoolExecutor and updates the UI via .after() to avoid thread-unsafe calls.

layout.py expects app to provide callbacks (e.g., run_model, open_menu_window, select_task).

Troubleshooting — common errors & fixes
Circular import / setup_layout error

If you see:

ImportError: cannot import name 'setup_layout' from partially initialized module 'gui.layout'

Fix: ensure gui/layout.py does not import gui.app. app.py should import setup_layout and call setup_layout(self) after constructing the app object. Use the provided files where layout.py only defines setup_layout(app).

Missing packages

Install missing packages into the active venv:

pip install customtkinter pillow transformers

If transformers is missing, GenSumAI will use fallback logic.

GUI freezes

If long model runs block the UI, ensure the code uses executor.submit() and updates the UI from the main thread using after() (the provided code already does this).

Assets, fonts & theming

Drop crisp PNG/SVG icons into gui/assets/ (e.g., logo.png, files.png, run.png).

Theme uses the Inter font stack by default. Install Inter (or SF Pro/Roboto) on your OS for best typography; system fallback will be used if not present.

Dark Mode is provided by customtkinter and toggled from the top-right switch.

Tests & manual checks

Manual checklist:

python3 main.py launches without tracebacks

Files/Menu opens and files are viewable

Compose area is resizable by dragging sash

Collapse/expand Compose works (Ctrl+T)

Run uses background thread; UI remains responsive

Activity panel logs actions

Shortcuts work (Ctrl+R, Ctrl+L, Ctrl+C, Ctrl+T)

Contributing

Fork repo

git checkout -b feat/your-feature

Implement changes & test locally

Open a pull request describing the change

Follow PEP8. Keep gui/layout.py free of imports that create circular dependencies.
