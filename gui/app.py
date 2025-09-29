import os
import customtkinter as ctk
from tkinter import messagebox, filedialog
from concurrent.futures import ThreadPoolExecutor
from functools import partial

from model.text_model import TextGenerator
from model.summary_model import Summarizer
from model.translation_model import TranslationModelAdapter
from model.image_model import ImageClassificationModelAdapter

from .icons import load_icons
from .theme import THEME, update_colors
from .layout import setup_layout

TEXT_FILE_EXTS = {".py", ".txt", ".md", ".json", ".cfg", ".ini", ".log", ".csv"}


class NLPApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(f"{THEME['APP_NAME']} v{THEME['VERSION']}")
        self.geometry("1220x780")
        self.minsize(1000, 680)

        assets_folder = os.path.join(os.path.dirname(__file__), "assets")
        self.icons = load_icons(assets_folder)

        # Initialize models
        try:
            self.models = {
                "Text Generation": TextGenerator("openai-community/gpt2"),
                "Summarization": Summarizer("facebook/bart-large-cnn"),
                "Translation": TranslationModelAdapter("French"),  # default
                "Image Classification": ImageClassificationModelAdapter(),
            }
        except Exception as e:
            messagebox.showerror("Error", f"Model initialization failed: {e}")
            self.destroy()
            return

        # Mapping: model_name -> task(s)
        self.model_name_to_task = {}
        for task, model in self.models.items():
            try:
                name = model.get_model_name()
            except Exception:
                name = str(model)
            self.model_name_to_task.setdefault(name, []).append(task)

        self.task_var = ctk.StringVar(value="Text Generation")

        # Translation dropdown support
        self.lang_var = ctk.StringVar(value="French")
        self.supported_languages = list(TranslationModelAdapter.SUPPORTED_MODELS.keys())
        self.lang_dropdown = None

        # Executor for background tasks
        self.executor = ThreadPoolExecutor(max_workers=1)

        setup_layout(self)
        self.select_task("Text Generation")

    # ------------------ task selection sync ------------------
    def on_model_selected(self, selected_model_name):
        if not selected_model_name:
            return
        tasks = self.model_name_to_task.get(selected_model_name, [])
        if "Text Generation" in tasks:
            chosen = "Text Generation"
        elif tasks:
            chosen = tasks[0]
        else:
            chosen = None

        if chosen:
            self.select_task(chosen)
            self.add_activity(
                f"Model selected: {selected_model_name} → switched to task: {chosen}"
            )
        else:
            self.add_activity(f"Model selected: {selected_model_name} (no task mapping)")

    def select_task(self, task):
        if isinstance(task, (tuple, list)):
            task = task[0] if task else "Text Generation"
        if not isinstance(task, str):
            task = str(task)
        self.task_var.set(task)

        try:
            self.task_segment.set(task)
        except Exception:
            pass

        try:
            model_name = self.models.get(task).get_model_name()
            if self.model_selector.get() != model_name:
                self.model_selector.set(model_name)
        except Exception:
            pass

        for t, btn in getattr(self, "task_buttons", {}).items():
            try:
                btn.configure(fg_color=THEME["PRIMARY"] if t == task else "transparent")
            except Exception:
                pass

        try:
            self.status_left.configure(text=f"Selected: {task}")
            self.add_activity(f"Selected task: {task}")
        except Exception:
            pass

        # --- Show dropdown only for Translation ---
        if task == "Translation":
            if self.lang_dropdown:
                self.lang_dropdown.pack(side="left", padx=6)
        else:
            if self.lang_dropdown:
                self.lang_dropdown.pack_forget()

    # ------------------ model run ------------------
    def _run_model_background(self, task, text):
        try:
            if task == "Text Generation":
                result = self.models[task].run(text, max_length=self.max_len.get())

            elif task == "Summarization":
                result = self.models[task].run(
                    text, max_length=self.max_len.get(), min_length=self.min_len.get()
                )

            elif task == "Translation":
                lang = self.lang_var.get()
                self.models["Translation"] = TranslationModelAdapter(lang)
                result = self.models["Translation"].run(text)

            elif task == "Image Classification":
                img_path = filedialog.askopenfilename(
                    title="Select an image",
                    filetypes=[("Image files", "*.jpg *.png *.jpeg *.bmp")],
                )
                if not img_path:
                    return False, "No image selected"
                pipeline = self.models[task]._build_pipeline()
                output = pipeline(img_path)
                result = self.models[task].postprocess(output)

            else:
                return False, f"Unknown task: {task}"

            return True, result

        except Exception as e:
            return False, str(e)

    def run_model(self):
        task = self.task_var.get()
        text = self.input_box.get("1.0", "end").strip()

        if task != "Image Classification" and not text:
            messagebox.showwarning("Warning", "Please enter some text first.")
            return

        try:
            self.run_button.configure(state="disabled")
        except Exception:
            pass

        self.status_left.configure(text=f"Processing: {task}...")
        self.status_right.configure(text="Working")
        self.progress.set(0.05)
        self.add_activity(f"Started {task}")

        future = self.executor.submit(self._run_model_background, task, text)

        def _done_callback(fut):
            success, payload = fut.result()
            self.after(10, lambda: self._on_model_done(success, payload, task))

        future.add_done_callback(_done_callback)

    def _on_model_done(self, success, payload, task):
        try:
            if success:
                self.output_box.delete("1.0", "end")
                self.output_box.insert("end", payload)
                self.progress.set(1.0)
                self.status_left.configure(text="Completed successfully")
                self.status_right.configure(text="Idle")
                self.add_activity(f"Completed: {task}")
            else:
                self.progress.set(0.0)
                messagebox.showerror("Error", f"Processing failed: {payload}")
                self.status_left.configure(text="Error occurred")
                self.status_right.configure(text="Idle")
                self.add_activity(f"Error: {payload}")
        finally:
            try:
                self.run_button.configure(state="normal")
            except Exception:
                pass
            self.after(600, lambda: self.progress.set(0.0))

    # ------------------ utilities ------------------
    def clear_all(self):
        try:
            self.input_box.delete("1.0", "end")
            self.output_box.delete("1.0", "end")
            self.progress.set(0.0)
            self.status_left.configure(text="Cleared")
            self.add_activity("Cleared input and output")
        except Exception:
            pass

    def copy_output(self):
        try:
            text = self.output_box.get("1.0", "end").strip()
            if text:
                self.clipboard_clear()
                self.clipboard_append(text)
                self.status_left.configure(text="Copied to clipboard")
                self.add_activity("Copied output to clipboard")
            else:
                self.status_left.configure(text="No output to copy")
        except Exception:
            pass

    def destroy(self):
        try:
            self.executor.shutdown(wait=False)
        except Exception:
            pass
        super().destroy()
