import customtkinter as ctk

THEME = {
    "APP_NAME": "GenSumAI",
    "VERSION": "1.0.0",

    # Colors
    "PRIMARY": "#2B7BE4",      # main blue
    "ACCENT": "#7AD3FF",       # lighter accent blue
    "SUCCESS": "#4CAF50",
    "WARN": "#FFB020",
    "ERROR": "#E14D4D",
    "HOVER": "#1F6FD0",

    # Background / card colors
    "BG_LIGHT": "#F5F7FA",
    "BG_DARK": "#1F2430",
    "CARD_LIGHT": "#FFFFFF",
    "CARD_DARK": "#2A303B",

    # Text colors
    "TEXT_LIGHT": "#22242A",
    "TEXT_DARK": "#E7E9EE",

    # Layout sizing
    "SIDEBAR_WIDTH": 300,
    "GAP": 14,
    "PADDING": 16,

    # Fonts
    "FONT_FAMILY": "Helvetica",
    "FONT_LG": ("Helvetica", 20, "bold"),
    "FONT_MD": ("Helvetica", 14),
    "FONT_SM": ("Helvetica", 12),

    # Extra style (for dropdowns etc.)
    "DROPDOWN": "#2B7BE4",
}

# ---------------- Global defaults ----------------
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


def update_colors(app):
    """
    Update widget colors dynamically depending on light/dark mode.
    Ensures consistency across sidebar, frames, text, and dropdowns.
    """
    is_dark = ctk.get_appearance_mode().lower() == "dark"
    bg_color = THEME["BG_DARK"] if is_dark else THEME["BG_LIGHT"]
    card_color = THEME["CARD_DARK"] if is_dark else THEME["CARD_LIGHT"]
    text_color = THEME["TEXT_DARK"] if is_dark else THEME["TEXT_LIGHT"]

    # Root background
    try:
        app.configure(fg_color=bg_color)
    except Exception:
        pass

    # Frames and panels
    for attr in (
        "sidebar",
        "input_frame",
        "output_frame",
        "right_panel",
        "statusbar",
    ):
        w = getattr(app, attr, None)
        if w is not None:
            try:
                w.configure(fg_color=card_color)
            except Exception:
                pass

    # Labels (titles, status, headers)
    for label_name in (
        "title_label",
        "input_label",
        "output_label",
        "status_left",
        "status_right",
    ):
        lbl = getattr(app, label_name, None)
        if lbl is not None:
            try:
                lbl.configure(text_color=text_color)
            except Exception:
                pass

    # Dropdown (language selector)
    if hasattr(app, "lang_dropdown") and app.lang_dropdown is not None:
        try:
            app.lang_dropdown.configure(
                fg_color=THEME["PRIMARY"],
                button_color=THEME["PRIMARY"],
                button_hover_color=THEME["HOVER"],
                text_color="white" if is_dark else "black",
                dropdown_fg_color=card_color,
                dropdown_text_color=text_color,
                dropdown_hover_color=THEME["ACCENT"],
            )
        except Exception:
            pass

    # Buttons → ensure consistent size & theme
    for btn_name in (
        "run_button",
        "batch_button",
        "clear_btn",
        "menu_btn",
        "image_browse_btn",
    ):
        btn = getattr(app, btn_name, None)
        if btn is not None:
            try:
                btn.configure(
                    fg_color=THEME["PRIMARY"],
                    hover_color=THEME["HOVER"],
                    text_color="white",
                    corner_radius=6,
                    height=36,
                )
            except Exception:
                pass
