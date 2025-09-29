import customtkinter as ctk
from tkinter import messagebox
from .theme import THEME


class ToolTip:
    def __init__(self, widget, text, delay=500):
        self.widget = widget
        self.text = text
        self.delay = delay
        self._id = None
        self._tip = None
        widget.bind("<Enter>", self._schedule)
        widget.bind("<Leave>", self._unschedule)

    def _schedule(self, _=None):
        self._unschedule()
        self._id = self.widget.after(self.delay, self._show)

    def _unschedule(self, _=None):
        if self._id:
            self.widget.after_cancel(self._id)
            self._id = None
        self._hide()

    def _show(self):
        if self._tip:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20
        self._tip = ctk.CTkToplevel(self.widget)
        self._tip.overrideredirect(True)
        self._tip.geometry(f"+{x}+{y}")
        lbl = ctk.CTkLabel(
            self._tip,
            text=self.text,
            font=THEME["FONT_SM"],
            corner_radius=6,
            fg_color=("gray85", THEME["CARD_DARK"]),
        )
        lbl.pack(padx=8, pady=6)

    def _hide(self):
        if self._tip:
            try:
                self._tip.destroy()
            except Exception:
                pass
            self._tip = None


def setup_layout(app):
    GAP = THEME["GAP"]
    P = THEME["PADDING"]

    # Sidebar
    app.sidebar = ctk.CTkFrame(
        app,
        width=THEME["SIDEBAR_WIDTH"],
        corner_radius=8,
        fg_color=("gray90", THEME["CARD_DARK"]),
    )
    app.sidebar.pack(side="left", fill="y", padx=(P, 0), pady=P)
    app.sidebar.pack_propagate(False)

    top_logo = ctk.CTkFrame(app.sidebar, fg_color="transparent")
    top_logo.pack(fill="x", pady=(P // 2, P))
    if app.icons.get("logo"):
        ctk.CTkLabel(top_logo, image=app.icons["logo"], text="").pack(
            side="left", padx=(4, 10)
        )
    app.title_label = ctk.CTkLabel(
        top_logo,
        text=THEME["APP_NAME"],
        font=THEME["FONT_LG"],
        text_color=(THEME["TEXT_LIGHT"], THEME["TEXT_DARK"]),
    )
    app.title_label.pack(side="left", anchor="w")

    task_container = ctk.CTkFrame(app.sidebar, fg_color="transparent")
    task_container.pack(fill="x", pady=(8, 12), padx=6)

    ctk.CTkLabel(
        task_container,
        text="TASKS",
        font=THEME["FONT_SM"],
        text_color=("gray60", "gray70"),
    ).pack(anchor="w", pady=(0, 8))
    app.task_buttons = {}
    for task in app.models.keys():
        if "Text" in task:
            icon = app.icons.get("gen")
        elif "Summarization" in task:
            icon = app.icons.get("sum")
        elif "Translation" in task:
            icon = app.icons.get("translate")
        elif "Image" in task:
            icon = app.icons.get("image")
        else:
            icon = None

        btn = ctk.CTkButton(
            task_container,
            text=task,
            image=icon,
            compound="left",
            width=THEME["SIDEBAR_WIDTH"] - 32,
            height=42,
            anchor="w",
            fg_color="transparent",
            hover_color=THEME["HOVER"],
            text_color=(THEME["TEXT_LIGHT"], THEME["TEXT_DARK"]),
            font=THEME["FONT_MD"],
            command=lambda t=task: app.select_task(t),
        )
        btn.pack(fill="x", pady=6)
        btn.bind("<Return>", lambda e, t=task: app.select_task(t))
        app.task_buttons[task] = btn

    sidebar_bottom = ctk.CTkFrame(app.sidebar, fg_color="transparent")
    sidebar_bottom.pack(side="bottom", fill="x", pady=P, padx=6)
    app.dark_mode_var = ctk.BooleanVar(
        value=(ctk.get_appearance_mode().lower() == "dark")
    )
    switch = ctk.CTkSwitch(
        sidebar_bottom,
        text="Dark Mode",
        variable=app.dark_mode_var,
        command=app.toggle_mode,
    )
    switch.pack(side="left")
    if app.icons.get("settings"):
        btn = ctk.CTkButton(
            sidebar_bottom,
            width=36,
            height=36,
            image=app.icons["settings"],
            fg_color="transparent",
            hover_color=("gray85", "gray25"),
            command=app.open_settings,
        )
        btn.pack(side="right", padx=6)
        ToolTip(btn, "Settings")

    # Main content
    main = ctk.CTkFrame(app, fg_color="transparent")
    main.pack(side="left", fill="both", expand=True, padx=(P, P // 2), pady=P)

    nav = ctk.CTkFrame(main, height=64, fg_color=("gray95", THEME["CARD_DARK"]))
    nav.pack(fill="x", pady=(0, 12))
    nav.pack_propagate(False)

    left_nav = ctk.CTkFrame(nav, fg_color="transparent")
    left_nav.pack(side="left", padx=6)
    ctk.CTkLabel(
        left_nav,
        text="Natural Language Processing",
        font=THEME["FONT_LG"],
        text_color=(THEME["TEXT_LIGHT"], THEME["TEXT_DARK"]),
    ).pack(anchor="w")

    center_nav = ctk.CTkFrame(nav, fg_color="transparent")
    center_nav.pack(side="left", expand=True)

    # Friendly model names
    model_names = []
    for m in app.models.values():
        if hasattr(m, "get_model_name"):
            try:
                model_names.append(m.get_model_name())
            except Exception:
                model_names.append(str(m))
        else:
            model_names.append(str(m))

    app.model_selector = ctk.CTkOptionMenu(
        center_nav, values=model_names, width=260, command=app.on_model_selected
    )
    try:
        default_model = app.models.get("Text Generation").get_model_name()
        app.model_selector.set(default_model)
    except Exception:
        if model_names:
            app.model_selector.set(model_names[0])
    app.model_selector.pack(side="left", padx=(6, 12))
    ToolTip(app.model_selector, "Select the underlying model")

    # Segmented task control
    app.task_segment = ctk.CTkSegmentedButton(
        center_nav, values=list(app.models.keys()), command=app.select_task
    )
    app.task_segment.set("Text Generation")
    app.task_segment.pack(side="left", padx=6)

    right_nav = ctk.CTkFrame(nav, fg_color="transparent")
    right_nav.pack(side="right", padx=6)
    app.run_button = ctk.CTkButton(
        right_nav,
        text="Run",
        width=100,
        command=app.run_model,
        image=app.icons.get("run"),
    )
    app.run_button.pack(side="left", padx=(6, 12))
    ToolTip(app.run_button, "Run the selected task (Ctrl+R)")
    clear_btn = ctk.CTkButton(
        right_nav,
        text="Clear",
        width=80,
        command=app.clear_all,
        image=app.icons.get("clear"),
    )
    clear_btn.pack(side="left", padx=6)
    ToolTip(clear_btn, "Clear input & output (Ctrl+L)")

    menu_btn = ctk.CTkButton(
        right_nav, text="Menu", width=80, command=app.open_menu_window
    )
    menu_btn.pack(side="left", padx=6)
    ToolTip(menu_btn, "Open Files & Menu (separate window)")

    # Content area
    content = ctk.CTkFrame(main, fg_color="transparent")
    content.pack(fill="both", expand=True)

    left_col = ctk.CTkFrame(content, fg_color="transparent")
    left_col.pack(side="left", fill="both", expand=True, padx=(0, 12))

    # Input card
    app.input_frame = ctk.CTkFrame(
        left_col, fg_color=("gray95", THEME["CARD_DARK"]), corner_radius=8
    )
    app.input_frame.pack(fill="x", pady=(0, 12))
    input_header = ctk.CTkFrame(app.input_frame, fg_color="transparent")
    input_header.pack(fill="x", padx=P, pady=(P // 2, 6))
    app.input_label = ctk.CTkLabel(
        input_header,
        text="Input Text",
        font=THEME["FONT_MD"],
        text_color=(THEME["TEXT_LIGHT"], THEME["TEXT_DARK"]),
    )
    app.input_label.pack(side="left")

    # Collapse/expand input
    app._input_collapsed = False
    def _toggle_input():
        if app._input_collapsed:
            app.input_box.pack(fill="both", padx=P, pady=(0, P))
            app._input_collapsed = False
            toggle_btn.configure(text="Hide")
            app.add_activity("Expanded input area")
        else:
            app.input_box.pack_forget()
            app._input_collapsed = True
            toggle_btn.configure(text="Show")
            app.add_activity("Collapsed input area")

    toggle_btn = ctk.CTkButton(input_header, text="Hide", width=64, command=_toggle_input)
    toggle_btn.pack(side="right")
    ToolTip(toggle_btn, "Hide/Show input area (Ctrl+T)")

    app.input_box = ctk.CTkTextbox(app.input_frame, height=200, font=THEME["FONT_MD"])
    app.input_box.pack(fill="both", padx=P, pady=(0, P))

    # Parameter toolbar
    toolbar = ctk.CTkFrame(left_col, fg_color="transparent")
    toolbar.pack(fill="x", pady=(0, 12))
    app.max_len = ctk.IntVar(value=150)
    app.min_len = ctk.IntVar(value=40)
    ctk.CTkLabel(toolbar, text="Max length:", font=THEME["FONT_SM"]).pack(
        side="left", padx=(0, 6)
    )
    ctk.CTkEntry(toolbar, textvariable=app.max_len, width=80, height=32).pack(
        side="left", padx=(0, 12)
    )
    ctk.CTkLabel(toolbar, text="Min length:", font=THEME["FONT_SM"]).pack(
        side="left", padx=(0, 6)
    )
    ctk.CTkEntry(toolbar, textvariable=app.min_len, width=80, height=32).pack(
        side="left", padx=(0, 12)
    )

    # Translation dropdown (hidden initially)
    app.lang_dropdown = ctk.CTkOptionMenu(
        toolbar, variable=app.lang_var, values=app.supported_languages, width=180
    )
    app.lang_dropdown.pack(side="left", padx=(12, 0))
    app.lang_dropdown.pack_forget()

    # Status / progress
    status_frame = ctk.CTkFrame(left_col, fg_color="transparent")
    status_frame.pack(fill="x", pady=(0, 12))
    app.progress = ctk.CTkProgressBar(status_frame, orientation="horizontal", width=300)
    app.progress.set(0.0)
    app.progress.pack(side="left", padx=(0, 12))
    app.status_left = ctk.CTkLabel(
        status_frame,
        text="Ready",
        font=THEME["FONT_SM"],
        text_color=("gray60", "gray70"),
    )
    app.status_left.pack(side="left")

    # Output card
    app.output_frame = ctk.CTkFrame(
        left_col, fg_color=("gray95", THEME["CARD_DARK"]), corner_radius=8
    )
    app.output_frame.pack(fill="both", expand=True)
    output_header = ctk.CTkFrame(app.output_frame, fg_color="transparent")
    output_header.pack(fill="x", padx=P, pady=(P // 2, 6))
    app.output_label = ctk.CTkLabel(
        output_header,
        text="Output",
        font=THEME["FONT_MD"],
        text_color=(THEME["TEXT_LIGHT"], THEME["TEXT_DARK"]),
    )
    app.output_label.pack(side="left")
    actions = ctk.CTkFrame(output_header, fg_color="transparent")
    actions.pack(side="right")
    ctk.CTkButton(
        actions,
        text="",
        width=36,
        height=36,
        image=app.icons.get("copy"),
        fg_color="transparent",
        command=app.copy_output,
    ).pack(side="left", padx=6)
    ctk.CTkButton(
        actions,
        text="",
        width=36,
        height=36,
        image=app.icons.get("close"),
        fg_color="transparent",
        command=lambda: app.output_box.delete("1.0", "end"),
    ).pack(side="left")
    ToolTip(actions, "Copy / Clear output")

    app.output_box = ctk.CTkTextbox(app.output_frame, font=THEME["FONT_MD"])
    app.output_box.pack(fill="both", expand=True, padx=P, pady=(0, P))

    # Right panel: Activity & History
    app.right_panel = ctk.CTkFrame(
        content, width=320, fg_color=("gray95", THEME["CARD_DARK"]), corner_radius=8
    )
    app.right_panel.pack(side="right", fill="y")
    app.right_panel.pack_propagate(False)

    rp_header = ctk.CTkFrame(app.right_panel, fg_color="transparent")
    rp_header.pack(fill="x", pady=(P // 2, 6), padx=P)
    ctk.CTkLabel(rp_header, text="Activity", font=THEME["FONT_MD"]).pack(side="left")
    if app.icons.get("history"):
        ctk.CTkLabel(rp_header, image=app.icons["history"], text="").pack(side="right")

    app.activity_list = ctk.CTkScrollableFrame(
        app.right_panel, fg_color="transparent", height=420
    )
    app.activity_list.pack(fill="both", expand=True, padx=P, pady=(0, P))

    def add_activity(text):
        item = ctk.CTkLabel(
            app.activity_list,
            text=text,
            anchor="w",
            wraplength=260,
            font=THEME["FONT_SM"],
        )
        item.pack(fill="x", pady=6, padx=6)

    add_activity("Welcome to NeuralFlow Studio — recent actions will appear here.")
    add_activity(
        "Tip: Use Ctrl+R to run, Ctrl+L to clear, Ctrl+C to copy output, Ctrl+T to toggle input."
    )

    # Status bar
    statusbar = ctk.CTkFrame(main, height=36, fg_color=("gray95", THEME["CARD_DARK"]))
    statusbar.pack(fill="x", pady=(12, 0))
    statusbar.pack_propagate(False)
    app.status_left = ctk.CTkLabel(
        statusbar, text="Ready", font=THEME["FONT_SM"], anchor="w"
    )
    app.status_left.pack(side="left", padx=P // 2)
    app.status_right = ctk.CTkLabel(
        statusbar, text="Idle", font=THEME["FONT_SM"], anchor="e"
    )
    app.status_right.pack(side="right", padx=P // 2)

    # Keyboard shortcuts
    app.bind_all("<Control-r>", lambda e: app.run_model())
    app.bind_all("<Control-R>", lambda e: app.run_model())
    app.bind_all("<Control-l>", lambda e: app.clear_all())
    app.bind_all("<Control-L>", lambda e: app.clear_all())
    app.bind_all("<Control-c>", lambda e: app.copy_output())
    app.bind_all("<Control-C>", lambda e: app.copy_output())
    app.bind_all("<Control-q>", lambda e: app.quit())
    app.bind_all("<Control-Q>", lambda e: app.quit())
    app.bind_all("<Control-t>", lambda e: _toggle_input())
    app.bind_all("<Control-T>", lambda e: _toggle_input())

    app.add_activity = add_activity

    from .theme import update_colors
    update_colors(app)
