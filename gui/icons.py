import os
import customtkinter as ctk

try:
    from PIL import Image
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False

def load_icons(assets_folder: str):
    icon_configs = {
        "logo": ("logo.png", (36, 36)),
        "gen": ("gen_icon.png", (20, 20)),
        "sum": ("sum_icon.png", (20, 20)),
        "settings": ("settings.png", (18, 18)),
        "info": ("info.png", (18, 18)),
        "copy": ("copy.png", (16, 16)),
        "clear": ("clear.png", (16, 16)),
        "run": ("run.png", (20, 20)),
        "history": ("history.png", (18, 18)),
        "model": ("model.png", (18, 18)),
        "close": ("close.png", (16, 16))
    }

    icons = {}
    for name, (filename, size) in icon_configs.items():
        path = os.path.join(assets_folder, filename)
        if PIL_AVAILABLE and os.path.exists(path):
            try:
                img = Image.open(path).convert("RGBA")
                icons[name] = ctk.CTkImage(light_image=img, dark_image=img, size=size)
            except Exception:
                icons[name] = None
        else:
            icons[name] = None

    return icons
