import customtkinter as ctk
from tkinter import messagebox
from text_model import TextGenerator
from summary_model import Summarizer
import os

# Optional image support
try:
    from PIL import Image
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False

# Theme and styling constants
THEME = {
    "APP_NAME": "NeuralFlow Studio",
    "VERSION": "1.0.0",
    "PRIMARY": "#4688f1",  # A more refined blue
    "HOVER": "#3570d0",    # Darker Blue
    "BG_LIGHT": "#f9f9fb",  # Very light gray for light mode
    "BG_DARK": "#242938",   # Dark Blue-Gray for dark mode
    "CARD_LIGHT": "#ffffff", # White for light mode cards
    "CARD_DARK": "#2d3343",  # Darker Blue-Gray for dark mode cards
    "TEXT_LIGHT": "#333333", # Dark Gray for light mode text
    "TEXT_DARK": "#d0d0d0",  # Light Gray for dark mode text
    "SIDEBAR_WIDTH": 260
}

ctk.set_appearance_mode("system")  # Use system default
ctk.set_default_color_theme("blue")

class NLPApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title(f"{THEME['APP_NAME']} v{THEME['VERSION']}")
        self.geometry("1080x720")
        self.minsize(900, 600)
        
        # Load icons
        self.load_icons()
        
        # Initialize models
        try:
            self.models = {
                "Text Generation": TextGenerator("openai-community/gpt2"),
                "Summarization": Summarizer("facebook/bart-large-cnn")
            }
        except Exception as e:
            messagebox.showerror("Error", f"Model loading failed: {e}")
            self.destroy()
            return

        self.task_var = ctk.StringVar(value="Text Generation")
        
        # Create layout
        self.setup_layout()
        self.select_task("Text Generation")

    def load_icons(self):
        """Load application icons"""
        self.icons = {}
        icon_configs = {
            "logo": ("logo.png", (36, 36)),
            "gen": ("gen_icon.png", (20, 20)),
            "sum": ("sum_icon.png", (20, 20)),
            "settings": ("settings.png", (18, 18)),
            "info": ("info.png", (18, 18)),
            "copy": ("copy.png", (16, 16)),
            "clear": ("clear.png", (16, 16)),
            "run": ("run.png", (20, 20))
        }

        for name, (filename, size) in icon_configs.items():
            path = os.path.join(os.path.dirname(__file__), "assets", filename)
            if os.path.exists(path) and PIL_AVAILABLE:
                try:
                    img = Image.open(path).convert("RGBA")
                    self.icons[name] = ctk.CTkImage(light_image=img, dark_image=img, size=size)
                except Exception:
                    self.icons[name] = None

    def setup_layout(self):
        """Create main application layout"""
        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=THEME["SIDEBAR_WIDTH"], corner_radius=0,
                                     fg_color=("gray90", THEME["BG_DARK"]))
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        # App header in sidebar
        header = ctk.CTkFrame(self.sidebar, fg_color="transparent", height=80)
        header.pack(fill="x", pady=(20, 25))
        header.pack_propagate(False)
        
        if self.icons.get("logo"):
            ctk.CTkLabel(header, image=self.icons["logo"], text="").pack(side="left", padx=(25, 10))
        
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left", fill="both", expand=True)
        self.title_label = ctk.CTkLabel(title_frame, text=THEME["APP_NAME"], 
                    font=("SF Pro Display", 20, "bold"),
                    text_color=(THEME["TEXT_LIGHT"], THEME["TEXT_DARK"]))
        self.title_label.pack(anchor="w")
        ctk.CTkLabel(title_frame, text="AI Language Processing",
                    font=("SF Pro Display", 12),
                    text_color=("gray70", "gray45")).pack(anchor="w")

        # Task section
        ctk.CTkLabel(self.sidebar, text="TASKS",
                    font=("SF Pro Display", 12, "bold"),
                    text_color=("gray70", "gray45")).pack(anchor="w", padx=25, pady=(0, 10))
        
        # Task buttons
        self.task_buttons = {}
        for task in self.models.keys():
            img = self.icons.get("gen") if "Text" in task else self.icons.get("sum")
            btn = ctk.CTkButton(self.sidebar, text=task, image=img,
                              font=("SF Pro Display", 13), height=45,
                              anchor="w", fg_color="transparent",
                              text_color=(THEME["TEXT_LIGHT"], THEME["TEXT_DARK"]),
                              hover_color=("gray85", "gray25"),
                              command=lambda t=task: self.select_task(t))
            btn.pack(fill="x", padx=12, pady=2)
            self.task_buttons[task] = btn

        # Bottom controls
        bottom = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        bottom.pack(side="bottom", fill="x", pady=20)
        
        self.dark_mode_var = ctk.BooleanVar(value=True)
        ctk.CTkSwitch(bottom, text="Dark Mode",
                     variable=self.dark_mode_var,
                     command=self.toggle_mode,
                     font=("SF Pro Display", 13)).pack(side="left", padx=20)

        if self.icons.get("settings"):
            ctk.CTkButton(bottom, text="", width=35, height=35,
                         image=self.icons["settings"],
                         fg_color="transparent",
                         hover_color=("gray85", "gray25"),
                         command=self.open_settings).pack(side="right", padx=20)

        # Main content area
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(side="left", fill="both", expand=True, padx=25, pady=20)

        # Main area header
        main_header = ctk.CTkFrame(main, fg_color="transparent", height=50)
        main_header.pack(fill="x", pady=(0, 20))
        main_header.pack_propagate(False)

        ctk.CTkLabel(main_header, text="Natural Language Processing",
                    font=("SF Pro Display", 24, "bold"),
                    text_color=(THEME["TEXT_LIGHT"], THEME["TEXT_DARK"])).pack(side="left")

        if self.icons.get("info"):
            ctk.CTkButton(main_header, text="", width=35, height=35,
                         image=self.icons["info"],
                         fg_color="transparent",
                         hover_color=("gray85", "gray25"),
                         command=self.show_about).pack(side="right")

        # Input section
        self.input_frame = ctk.CTkFrame(main, fg_color=("gray90", THEME["CARD_DARK"]))
        self.input_frame.pack(fill="x", pady=(0, 15))
        
        input_header = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        input_header.pack(fill="x", padx=15, pady=10)
        self.input_label = ctk.CTkLabel(input_header, text="Input Text",
                    font=("SF Pro Display", 14, "bold"),
                    text_color=(THEME["TEXT_LIGHT"], THEME["TEXT_DARK"]))
        self.input_label.pack(side="left")

        self.input_box = ctk.CTkTextbox(self.input_frame, height=150,
                                      font=("SF Pro Display", 13),
                                      text_color=(THEME["TEXT_LIGHT"], THEME["TEXT_DARK"]))
        self.input_box.pack(fill="x", padx=15, pady=(0, 15))

        # Controls section
        self.controls = ctk.CTkFrame(main, fg_color=("gray90", THEME["CARD_DARK"]))
        self.controls.pack(fill="x", pady=(0, 15))

        # Parameters
        param_frame = ctk.CTkFrame(self.controls, fg_color="transparent")
        param_frame.pack(side="left", padx=15, pady=10)

        self.max_len = ctk.IntVar(value=150)
        self.min_len = ctk.IntVar(value=40)

        for i, (label, var) in enumerate([("Max Length", self.max_len),
                                        ("Min Length", self.min_len)]):
            ctk.CTkLabel(param_frame, text=label,
                        font=("SF Pro Display", 13),
                        text_color=(THEME["TEXT_LIGHT"], THEME["TEXT_DARK"])).grid(row=0, column=i*2, padx=5)
            ctk.CTkEntry(param_frame, textvariable=var,
                        width=70, height=32,
                        font=("SF Pro Display", 13),
                        text_color=(THEME["TEXT_LIGHT"], THEME["TEXT_DARK"])).grid(row=0, column=i*2+1, padx=5)

        # Action buttons
        action_frame = ctk.CTkFrame(self.controls, fg_color="transparent")
        action_frame.pack(side="right", padx=15, pady=10)

        button_configs = [
            ("Run", self.icons.get("run"), self.run_model, THEME["PRIMARY"], 100),
            ("Clear", self.icons.get("clear"), self.clear_all, None, 80),
            ("Copy", self.icons.get("copy"), self.copy_output, None, 80)
        ]

        for text, icon, command, color, width in button_configs:
            ctk.CTkButton(action_frame, text=text, image=icon,
                         command=command, width=width, height=32,
                         fg_color=color if color else "transparent",
                         text_color=(THEME["TEXT_LIGHT"], THEME["TEXT_DARK"]),
                         hover_color=THEME["HOVER"],
                         font=("SF Pro Display", 13)).pack(side="left", padx=5)

        # Output section
        self.output_frame = ctk.CTkFrame(main, fg_color=("gray90", THEME["CARD_DARK"]))
        self.output_frame.pack(fill="both", expand=True)
        
        output_header = ctk.CTkFrame(self.output_frame, fg_color="transparent")
        output_header.pack(fill="x", padx=15, pady=10)
        self.output_label = ctk.CTkLabel(output_header, text="Output",
                    font=("SF Pro Display", 14, "bold"),
                    text_color=(THEME["TEXT_LIGHT"], THEME["TEXT_DARK"]))
        self.output_label.pack(side="left")

        self.output_box = ctk.CTkTextbox(self.output_frame,
                                       font=("SF Pro Display", 13),
                                       text_color=(THEME["TEXT_LIGHT"], THEME["TEXT_DARK"]))
        self.output_box.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Status bar
        self.status = ctk.CTkLabel(main, text="Ready",
                                 font=("SF Pro Display", 12),
                                 text_color=("gray70", "gray45"))
        self.status.pack(fill="x", pady=(15, 0))

    def select_task(self, task):
        """Handle task selection"""
        self.task_var.set(task)
        for t, btn in self.task_buttons.items():
            btn.configure(fg_color=THEME["PRIMARY"] if t == task else "transparent")
        self.status.configure(text=f"Selected: {task}")

    def toggle_mode(self):
        """Toggle dark/light mode"""
        mode = "dark" if self.dark_mode_var.get() else "light"
        ctk.set_appearance_mode(mode)
        self.update_colors()
        self.status.configure(text=f"Theme: {mode.title()} mode")

    def update_colors(self):
        """Update colors based on the current mode"""
        is_dark = ctk.get_appearance_mode() == "Dark"
        bg_color = THEME["BG_DARK"] if is_dark else THEME["BG_LIGHT"]
        card_color = THEME["CARD_DARK"] if is_dark else THEME["CARD_LIGHT"]
        text_color = THEME["TEXT_DARK"] if is_dark else THEME["TEXT_LIGHT"]

        self.sidebar.configure(fg_color=("gray90", bg_color))
        self.input_frame.configure(fg_color=("gray90", card_color))
        self.controls.configure(fg_color=("gray90", card_color))
        self.output_frame.configure(fg_color=("gray90", card_color))

        # Update text colors
        self.title_label.configure(text_color=text_color)
        self.input_label.configure(text_color=text_color)
        self.output_label.configure(text_color=text_color)

    def open_settings(self):
        """Show settings dialog"""
        messagebox.showinfo("Settings", 
                          "Configure application settings\n\nComing soon...")

    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo("About",
                          f"{THEME['APP_NAME']} v{THEME['VERSION']}\n\n"
                          "Advanced Natural Language Processing Studio\n"
                          "Powered by state-of-the-art AI models")

    def run_model(self):
        """Execute the selected NLP task"""
        task = self.task_var.get()
        text = self.input_box.get("1.0", "end").strip()
        
        if not text:
            messagebox.showwarning("Warning", "Please enter some text first")
            return

        self.status.configure(text=f"Processing: {task}...")
        self.output_box.delete("1.0", "end")
        self.output_box.insert("end", "Processing...\n")
        self.update_idletasks()

        try:
            if task == "Text Generation":
                result = self.models[task].run(text, max_length=self.max_len.get())
            else:
                result = self.models[task].run(text, 
                                             max_length=self.max_len.get(),
                                             min_length=self.min_len.get())
            
            self.output_box.delete("1.0", "end")
            self.output_box.insert("end", result)
            self.status.configure(text="Completed successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Processing failed: {str(e)}")
            self.status.configure(text="Error occurred")

    def clear_all(self):
        """Clear input and output"""
        self.input_box.delete("1.0", "end")
        self.output_box.delete("1.0", "end")
        self.status.configure(text="Cleared all content")

    def copy_output(self):
        """Copy output to clipboard"""
        text = self.output_box.get("1.0", "end").strip()
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)
            self.status.configure(text="Copied to clipboard")
        else:
            self.status.configure(text="No output to copy")

if __name__ == "__main__":
    app = NLPApp()
    app.mainloop()