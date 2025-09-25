import customtkinter as ctk

THEME = {
    "APP_NAME": "GenSumAI",
    "VERSION": "1.0.0",
    "PRIMARY": "#2B7BE4",
    "ACCENT": "#7AD3FF",
    "SUCCESS": "#4CAF50",
    "WARN": "#FFB020",
    "ERROR": "#E14D4D",
    "HOVER": "#1F6FD0",
    "BG_LIGHT": "#F5F7FA",
    "BG_DARK": "#1F2430",
    "CARD_LIGHT": "#FFFFFF",
    "CARD_DARK": "#2A303B",
    "TEXT_LIGHT": "#22242A",
    "TEXT_DARK": "#E7E9EE",
    "SIDEBAR_WIDTH": 300,
    "GAP": 14,
    "PADDING": 16,
    "FONT_FAMILY": "Helvetica",
    "FONT_LG": ("Helvetica", 20, "bold"),
    "FONT_MD": ("Helvetica", 14),
    "FONT_SM": ("Helvetica", 12),
}

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")


def update_colors(app):
    is_dark = ctk.get_appearance_mode().lower() == "dark"
    bg_color = THEME["BG_DARK"] if is_dark else THEME["BG_LIGHT"]
    card_color = THEME["CARD_DARK"] if is_dark else THEME["CARD_LIGHT"]
    text_color = THEME["TEXT_DARK"] if is_dark else THEME["TEXT_LIGHT"]

    try:
        app.configure(fg_color=bg_color)
    except Exception:
        pass

    for attr in ("sidebar", "input_frame", "controls", "output_frame", "right_panel"):
        w = getattr(app, attr, None)
        if w is not None:
            try:
                w.configure(fg_color=("gray90", card_color))
            except Exception:
                pass

    for label_name in ("title_label", "input_label", "output_label", "status_left", "status_right"):
        lbl = getattr(app, label_name, None)
        if lbl is not None:
            try:
                lbl.configure(text_color=text_color)
            except Exception:
                pass
