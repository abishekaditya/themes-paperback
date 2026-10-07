#!/usr/bin/env python3
"""Generate Paperback .pbcolors themes from popular editor colour schemes.

Each scheme gets three files, matching the rest of the repo:
  <Folder>/<Name>-Theme-Paperback.pbcolors                     standard
  <Folder>/Black_Dark_Mode/<Name>-Theme-BDM-Paperback.pbcolors pitch-black dark mode
  <Folder>/Black_All_Modes/<Name>-Theme-BAM-Paperback.pbcolors pitch-black in both modes

Run from the repo root: python3 tools/generate_themes.py
"""

import json
import os

CREATOR = "abishekaditya"

# Per-mode palette: bg, surface (cards), border, text, subtext, accent,
# on_accent (text drawn on the accent colour), overlay.
CATPPUCCIN_LATTE = dict(bg="#eff1f5", surface="#ccd0da", border="#bcc0cc", text="#4c4f69",
                        subtext="#6c6f85", accent="#8839ef", on_accent="#eff1f5", overlay="#9ca0b0")
KANAGAWA_LOTUS = dict(bg="#f2ecbc", surface="#e5ddb0", border="#dcd5ac", text="#545464",
                      subtext="#716e61", accent="#4d699b", on_accent="#f2ecbc", overlay="#8a8980")

SCHEMES = [
    ("Catppuccin", "Catppuccin-Frappe", "Catppuccin Frappé (Latte in light mode)", CATPPUCCIN_LATTE,
     dict(bg="#303446", surface="#414559", border="#51576d", text="#c6d0f5",
          subtext="#a5adce", accent="#ca9ee6", on_accent="#232634", overlay="#737994")),
    ("Catppuccin", "Catppuccin-Macchiato", "Catppuccin Macchiato (Latte in light mode)", CATPPUCCIN_LATTE,
     dict(bg="#24273a", surface="#363a4f", border="#494d64", text="#cad3f5",
          subtext="#a5adcb", accent="#c6a0f6", on_accent="#181926", overlay="#6e738d")),
    ("Catppuccin", "Catppuccin-Mocha", "Catppuccin Mocha (Latte in light mode)", CATPPUCCIN_LATTE,
     dict(bg="#1e1e2e", surface="#313244", border="#45475a", text="#cdd6f4",
          subtext="#a6adc8", accent="#cba6f7", on_accent="#11111b", overlay="#6c7086")),
    ("Gruvbox", "Gruvbox", "Gruvbox",
     dict(bg="#fbf1c7", surface="#ebdbb2", border="#d5c4a1", text="#3c3836",
          subtext="#7c6f64", accent="#af3a03", on_accent="#fbf1c7", overlay="#a89984"),
     dict(bg="#282828", surface="#3c3836", border="#504945", text="#ebdbb2",
          subtext="#a89984", accent="#fe8019", on_accent="#282828", overlay="#928374")),
    ("Kanagawa", "Kanagawa-Wave", "Kanagawa Wave (Lotus in light mode)", KANAGAWA_LOTUS,
     dict(bg="#1f1f28", surface="#2a2a37", border="#363646", text="#dcd7ba",
          subtext="#c8c093", accent="#7e9cd8", on_accent="#1f1f28", overlay="#54546d")),
    ("Kanagawa", "Kanagawa-Dragon", "Kanagawa Dragon (Lotus in light mode)", KANAGAWA_LOTUS,
     dict(bg="#181616", surface="#282727", border="#393836", text="#c5c9c5",
          subtext="#a6a69c", accent="#8ba4b0", on_accent="#181616", overlay="#625e5a")),
    ("Monokai", "Monokai", "Monokai (Monokai Pro Light in light mode)",
     dict(bg="#faf4f2", surface="#ede7e5", border="#d3cdcc", text="#29242a",
          subtext="#706b6e", accent="#e14775", on_accent="#faf4f2", overlay="#a59fa0"),
     dict(bg="#272822", surface="#3e3d32", border="#49483e", text="#f8f8f2",
          subtext="#cfcfc2", accent="#f92672", on_accent="#272822", overlay="#75715e")),
    ("Nord", "Nord", "Nord",
     dict(bg="#eceff4", surface="#e5e9f0", border="#d8dee9", text="#2e3440",
          subtext="#4c566a", accent="#5e81ac", on_accent="#eceff4", overlay="#9aa5b8"),
     dict(bg="#2e3440", surface="#3b4252", border="#434c5e", text="#eceff4",
          subtext="#d8dee9", accent="#88c0d0", on_accent="#2e3440", overlay="#4c566a")),
    ("One_Dark", "One-Dark", "One Dark (One Light in light mode)",
     dict(bg="#fafafa", surface="#f0f0f0", border="#e5e5e6", text="#383a42",
          subtext="#696c77", accent="#4078f2", on_accent="#fafafa", overlay="#a0a1a7"),
     dict(bg="#282c34", surface="#2c313c", border="#3e4451", text="#dcdfe4",
          subtext="#9da5b4", accent="#61afef", on_accent="#282c34", overlay="#5c6370")),
]

BLACK = "#000000"


def rgba(hex_color, alpha=1):
    h = hex_color.lstrip("#")
    r, g, b = (round(int(h[i:i + 2], 16) / 255, 3) for i in (0, 2, 4))
    return {"red": r, "green": g, "blue": b, "alpha": alpha}


def slots(p):
    """Map a palette onto Paperback's colour slots as (hex, alpha) pairs."""
    return {
        "accentColor": (p["accent"], 1),
        "accentColorLight": (p["accent"], 1),
        "accentTextColor": (p["on_accent"], 1),
        "foregroundColor": (p["surface"], 1),
        "backgroundColor": (p["bg"], 1),
        "overlayColor": (p["overlay"], 0.3),
        "separatorColor": (p["accent"], 1),
        "borderColor": (p["border"], 1),
        "titleTextColor": (p["text"], 1),
        "supertitleTextColor": (p["subtext"], 1),
        "bodyTextColor": (p["text"], 1),
        "subtitleTextColor": (p["subtext"], 1),
        "buttonNormalBackgroundColor": (p["accent"], 0.3),
        "buttonNormalTextColor": (p["text"], 1),
        "buttonNormalBorderColor": (p["accent"], 1),
        "buttonSelectedBackgroundColor": (p["accent"], 0.5),
        "buttonSelectedTextColor": (p["text"], 1),
        "buttonSelectedBorderColor": (p["accent"], 1),
    }


def theme(description, light, dark):
    out = {"description": description, "creator": CREATOR}
    ls, ds = slots(light), slots(dark)
    for key in ls:
        out[key] = {"lightColor": rgba(*ls[key]), "darkColor": rgba(*ds[key])}
    return out


def write(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent="\t", ensure_ascii=False)
        f.write("\n")


def main():
    for folder, name, label, light, dark in SCHEMES:
        black_dark = dict(dark, bg=BLACK)
        write(f"{folder}/{name}-Theme-Paperback.pbcolors",
              theme(f"{label} theme for Paperback.", light, dark))
        write(f"{folder}/Black_Dark_Mode/{name}-Theme-BDM-Paperback.pbcolors",
              theme(f"{label} theme with black dark mode for Paperback.", light, black_dark))
        # Black in light mode too, so light mode uses the dark palette's text colours.
        write(f"{folder}/Black_All_Modes/{name}-Theme-BAM-Paperback.pbcolors",
              theme(f"{label} theme with black for all modes for Paperback.", black_dark, black_dark))


if __name__ == "__main__":
    main()
