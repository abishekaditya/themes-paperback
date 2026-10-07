#!/usr/bin/env python3
"""Convert every Paperback 0.8 .pbcolors theme in the repo to the 0.9 format.

Paperback 0.9 renamed and expanded the colour keys (background, foreground,
text, textSecondary, primary, ...). Each 0.8 theme at <path> is written to
Paperback_0.9/<path> with the same file name.

Paperback 0.9 only imports a theme file named themeColors.pbcolors, so rename
the downloaded file (the Pages site does this for you) before opening it.

Key roles follow https://github.com/LucifersCircle/theme-editor/blob/main/docs/paperback-v09-color-map.md

Run from the repo root after tools/generate_themes.py:
    python3 tools/convert_to_v09.py
"""

import glob
import json
import os

OUT_DIR = "Paperback_0.9"

# Paperback 0.9 defaults for status colours, which have no 0.8 equivalent.
STATUS = {
    "alert": ({"red": 1, "green": 0.22, "blue": 0.235}, {"red": 1, "green": 0.259, "blue": 0.271}),
    "error": ({"red": 1, "green": 0.22, "blue": 0.235}, {"red": 1, "green": 0.259, "blue": 0.271}),
    "warning": ({"red": 1, "green": 0.553, "blue": 0.157}, {"red": 1, "green": 0.573, "blue": 0.188}),
    "success": ({"red": 0.204, "green": 0.78, "blue": 0.349}, {"red": 0.188, "green": 0.82, "blue": 0.345}),
}


def with_alpha(color, alpha):
    return dict(color, alpha=alpha)


def convert_mode(old, mode):
    c = lambda key: old[key][mode]
    return {
        "background": c("backgroundColor"),
        "tertiary": c("backgroundColor"),
        "foreground": c("foregroundColor"),
        "border": c("borderColor"),
        "text": c("bodyTextColor"),
        "textSecondary": c("subtitleTextColor"),
        "textTertiary": c("supertitleTextColor"),
        "tertiaryText": c("supertitleTextColor"),
        "accent": c("accentColor"),
        "primary": c("accentColor"),
        "primaryText": c("accentTextColor"),
        "secondary": with_alpha(c("accentColor"), 0.15),
        "secondaryText": c("accentColor"),
        "alertText": c("accentTextColor"),
        "separator": with_alpha(c("bodyTextColor"), 0.1),
        "overlay": {"red": 0, "green": 0, "blue": 0, "alpha": 0.15},
    }


def convert(old, black_all_modes):
    # Black All Modes themes are dark in both appearances, so reuse the dark
    # palette for light mode too (0.8 BAM files kept some dark-on-black text).
    light = convert_mode(old, "darkColor" if black_all_modes else "lightColor")
    dark = convert_mode(old, "darkColor")
    out = {key: {"lightColor": light[key], "darkColor": dark[key]} for key in light}
    for key, (light_status, dark_status) in STATUS.items():
        out[key] = {"lightColor": dict(light_status, alpha=1), "darkColor": dict(dark_status, alpha=1)}
    return dict(sorted(out.items()))


def main():
    for path in sorted(glob.glob("**/*.pbcolors", recursive=True)):
        if path.startswith(OUT_DIR + os.sep):
            continue
        with open(path) as f:
            old = json.load(f)
        dest = os.path.join(OUT_DIR, path)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w") as f:
            json.dump(convert(old, "-BAM-" in os.path.basename(path)), f, indent="\t")
            f.write("\n")


if __name__ == "__main__":
    main()
