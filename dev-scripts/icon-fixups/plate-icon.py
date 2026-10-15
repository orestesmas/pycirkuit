#!/usr/bin/env python3
"""
Bake a small fixed-light "plate" behind a PNG icon's existing artwork.

Some bundled icons (e.g. Configure-export-image.png, application-x-pycirkuit.png)
are black/near-black line art on a transparent background, authored assuming
they'd sit on a light backdrop. That assumption broke when the UI started
following the system palette (see commit history around 2026-10): under a
dark theme the artwork became invisible against the now-dark background.

Their SVGZ sources are messy multi-artboard Illustrator exports (huge,
unrelated coordinate spaces clipped by viewBox) that are too fragile to
hand-edit safely. Instead, this composites a fixed-color rounded-rect plate
directly behind the already-correct PNG, sized to the artwork's own alpha
bounding box (+ padding), so the icon keeps a guaranteed-light backdrop no
matter the application's theme.

Usage:
    dev-scripts/icon-fixups/plate-icon.py <in.png> <out.png> [--pad N] [--radius N]

After regenerating affected PNGs, rebuild the embedded resource bundle:
    cd pycirkuit/resources && pyside6-rcc resources.qrc -o resources_rc.py
"""
import argparse
from PIL import Image, ImageDraw

PLATE_RGBA = (248, 248, 248, 255)
BORDER_RGBA = (190, 190, 190, 180)


def plated(path_in, path_out, pad, radius, border_w=1):
    im = Image.open(path_in).convert("RGBA")
    bbox = im.split()[-1].getbbox() or (0, 0, im.width, im.height)
    x0, y0, x1, y1 = bbox
    x0, y0 = max(0, x0 - pad), max(0, y0 - pad)
    x1, y1 = min(im.width, x1 + pad), min(im.height, y1 + pad)

    plate = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(plate).rounded_rectangle(
        [x0, y0, x1 - 1, y1 - 1], radius=radius, fill=PLATE_RGBA, outline=BORDER_RGBA, width=border_w
    )
    Image.alpha_composite(plate, im).save(path_out)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("input")
    p.add_argument("output")
    p.add_argument("--pad", type=int, default=3)
    p.add_argument("--radius", type=int, default=6)
    args = p.parse_args()
    plated(args.input, args.output, args.pad, args.radius)
