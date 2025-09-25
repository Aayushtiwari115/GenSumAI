import os
import customtkinter as ctk
from tkinter import messagebox
from concurrent.futures import ThreadPoolExecutor
from functools import partial

from model.text_model import TextGenerator
from model.summary_model import Summarizer

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
                "Summarization": Summarizer("facebook/bart-large-cnn")
            }
        except Exception as e:
            messagebox.showerror("Error", f"Model initialization failed: {e}")
            self.destroy()
            return

        # build mapping: model_name -> task(s)
        self.model_name_to_task = {}
        for task, model in self.models.items():
            try:
                name = model.get_model_name()
            except Exception:
                name = str(model)
            self.model_name_to_task.setdefault(name, []).append(task)

        self.task_var = ctk.StringVar(value="Text Generation")

        # executor for background tasks
        self.executor = ThreadPoolExecutor(max_workers=1)

        setup_layout(self)
        self.select_task("Text Generation")

    # ------------- two-way sync ----------------------------------------------
    def on_model_selected(self, selected_model_name):
        """
        Called when user picks a model in the model_selector. If a task is associated,
        automatically switch to that task (prioritise Text Generation if multiple).
        """
        if not selected_model_name:
            return
        tasks = self.model_name_to_task.get(selected_model_name, [])
        # prefer "Text Generation" if it's one of the tasks
        if "Text Generation" in tasks:
            chosen = "Text Generation"
        elif tasks:
            chosen = tasks[0]
        else:
            # no mapping found: do nothing but show current model selection
            chosen = None

        if chosen:
            self.select_task(chosen)
            self.add_activity(f"Model selected: {selected_model_name} → switched to task: {chosen}")
        else:
            self.add_activity(f"Model selected: {selected_model_name} (no task mapping)")

    def select_task(self, task):
        """
        Accepts direct strings (from sidebar), or the CTkSegmentedButton passes a single arg
        or tuple — handle gracefully.
        """
        if isinstance(task, (tuple, list)):
            task = task[0] if task else "Text Generation"
        if not isinstance(task, str):
            task = str(task)
        self.task_var.set(task)
        # sync segmented control
        try:
            self.task_segment.set(task)
        except Exception:
            pass
        # update model selector when task changes
        try:
            model_name = self.models.get(task).get_model_name()
            # only set option menu if it's different
            try:
                if self.model_selector.get() != model_name:
                    self.model_selector.set(model_name)
            except Exception:
                pass
        except Exception:
            pass

        # highlight sidebar button
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

    # ------------- settings / about -----------------------------------------
    def toggle_mode(self):
        mode = "dark" if self.dark_mode_var.get() else "light"
        ctk.set_appearance_mode(mode)
        update_colors(self)
        try:
            self.status_right.configure(text=f"{mode.title()} mode")
        except Exception:
            pass

    def open_settings(self):
        dlg = ctk.CTkToplevel(self)
        dlg.title("Settings")
        dlg.geometry("520x360")
        ctk.CTkLabel(dlg, text="Application Settings", font=THEME["FONT_LG"]).pack(padx=20, pady=16)
        ctk.CTkLabel(dlg, text="Configure model/autosave/logging here.", font=THEME["FONT_MD"]).pack(padx=20, pady=6)
        # Example toggles
        save_var = ctk.BooleanVar(value=False)
        autosave = ctk.CTkCheckBox(dlg, text="Autosave history", variable=save_var)
        autosave.pack(pady=6, padx=20, anchor="w")
        ctk.CTkButton(dlg, text="Close", command=dlg.destroy).pack(side="bottom", pady=16)

    def show_about(self):
        messagebox.showinfo("About", f"{THEME['APP_NAME']} v{THEME['VERSION']}\nDesigned for professional workflows.")

    # ------------- I/O: Files & Menu window ---------------------------------
    def open_menu_window(self):
        """
        Opens a separate Toplevel window with two tabs:
          - Files: shows project assets and allows viewing text file contents
          - Menu: quick actions (Settings, About, Quit)
        """
        win = ctk.CTkToplevel(self)
        win.title("Menu & Files")
        win.geometry("760x520")

        from customtkinter import CTkTabview
        tabs = CTkTabview(win, width=740, height=480)
        tabs.pack(padx=10, pady=10, fill="both", expand=True)
        tabs.add("Files")
        tabs.add("Menu")

        # Files tab content
        files_frame = ctk.CTkFrame(tabs.tab("Files"))
        files_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # List assets folder first, then project root text files
        assets_dir = os.path.join(os.path.dirname(__file__), "assets")
        items = []
        if os.path.isdir(assets_dir):
            assets = sorted(os.listdir(assets_dir))
            if assets:
                items.append(("Assets", assets_dir, assets))
        # project root text files
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        project_files = []
        for fn in sorted(os.listdir(project_root)):
            fp = os.path.join(project_root, fn)
            if os.path.isfile(fp):
                project_files.append(fn)
        if project_files:
            items.append(("Project", project_root, project_files))

        list_container = ctk.CTkScrollableFrame(files_frame, width=700, height=420)
        list_container.pack(fill="both", expand=True)
        for title, folder, files in items:
            hdr = ctk.CTkLabel(list_container, text=title, font=THEME["FONT_MD"], anchor="w")
            hdr.pack(fill="x", pady=(6,0), padx=6)
            for fn in files:
                fp = os.path.join(folder, fn)
                display = f" {fn}"
                btn = ctk.CTkButton(list_container, text=display, anchor="w", fg_color="transparent",
                                     hover_color=("gray85", "gray25"),
                                     command=partial(self.open_file_viewer, fp))
                btn.pack(fill="x", padx=8, pady=2)

        # Menu tab content
        menu_frame = ctk.CTkFrame(tabs.tab("Menu"))
        menu_frame.pack(fill="both", expand=True, padx=10, pady=10)
        ctk.CTkButton(menu_frame, text="Open Settings", command=self.open_settings).pack(pady=8, padx=12, anchor="w")
        ctk.CTkButton(menu_frame, text="About", command=self.show_about).pack(pady=8, padx=12, anchor="w")
        ctk.CTkButton(menu_frame, text="Quit", command=self.quit).pack(pady=8, padx=12, anchor="w")

    def open_file_viewer(self, filepath):
        """
        Open a simple viewer window for text files. If binary or unreadable, inform the user.
        """
        try:
            ext = os.path.splitext(filepath)[1].lower()
            if ext not in TEXT_FILE_EXTS:
                # Try to read but guard
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                except Exception:
                    messagebox.showinfo("Cannot open file", f"Unable to open {os.path.basename(filepath)} (binary or unsupported).")
                    return
            else:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
        except Exception as e:
            messagebox.showinfo("Error", f"Failed to open file: {e}")
            return

        win = ctk.CTkToplevel(self)
        win.title(os.path.basename(filepath))
        win.geometry("760x520")
        text = ctk.CTkTextbox(win, font=THEME["FONT_MD"])
        text.pack(fill="both", expand=True, padx=10, pady=10)
        text.insert("1.0", content)
        text.configure(state="disabled")
        ctk.CTkButton(win, text="Close", command=win.destroy).pack(pady=8)

    # ------------- Model run (background) -----------------------------------
    def _run_model_background(self, task, text):
        """
        This runs inside a worker thread. Return a tuple (success, result_or_exception_str).
        """
        try:
            if task == "Text Generation":
                result = self.models[task].run(text, max_length=self.max_len.get())
            else:
                result = self.models[task].run(text, max_length=self.max_len.get(), min_length=self.min_len.get())
            return True, result
        except Exception as e:
            return False, str(e)

    def run_model(self):
        """
        Public: schedule model run on background thread and update UI when done.
        """
        task = self.task_var.get()
        text = self.input_box.get("1.0", "end").strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter some text first.")
            return

        # disable run button while running
        try:
            self.run_button.configure(state="disabled")
        except Exception:
            pass
        self.status_left.configure(text=f"Processing: {task}...")
        self.status_right.configure(text="Working")
        self.progress.set(0.05)
        self.add_activity(f"Started {task}")

        future = self.executor.submit(self._run_model_background, task, text)

        # after completion callback (schedules UI update in main thread)
        def _done_callback(fut):
            success, payload = fut.result()
            self.after(10, lambda: self._on_model_done(success, payload, task))

        future.add_done_callback(_done_callback)

    def _on_model_done(self, success, payload, task):
        """
        Called on the main thread after the background model finishes.
        """
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
            # gently reset progress bar after short delay
            self.after(600, lambda: self.progress.set(0.0))

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

    # cleanup
    def destroy(self):
        try:
            self.executor.shutdown(wait=False)
        except Exception:
            pass
        super().destroy()
