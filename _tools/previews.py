import os
from PIL import Image

# Build the layered home-page preview assets: crop a region (source pixels) and scale to a max width.
#   (output name, source image, (x0, y0, x1, y1) or None for the whole image, max output width)
JOBS = [
    ("pv-lm-base",  "_private/liquidity-img/lm-cards.webp",     (0, 40, 2000, 940),     1400),
    ("pv-lm-float", "_private/liquidity-img/lm-execute.webp",   (30, 360, 500, 634),    760),
    ("pv-sw-base",  "_private/swap-img/sw-offers.png",          (120, 118, 1080, 807),  1100),
    ("pv-sw-float", "_private/swap-img/sw-breakdown.png",       (770, 262, 1042, 552),  560),
    ("pv-er-base",  "_private/earn-img/er-choose.png",          (0, 80, 2880, 1380),    1400),
    ("pv-er-float", "_private/earn-img/er-deposit.png",         (2170, 300, 2880, 1290),620),
    ("pv-vm-base",  "site/img/vm-cover.jpg",                    None,                   1600),
    ("pv-vm-float", "site/img/vm-automation.jpg",               (1604, 411, 2491, 822), 900),
    ("pv-cal-float","site/img/cal-cards.jpg",                   (723, 17, 1469, 1339),  520),
]

for name, src, box, max_w in JOBS:
    im = Image.open(src)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[-1])
        im = bg
    else:
        im = im.convert("RGB")
    if box:
        im = im.crop(box)
    if im.width > max_w:
        im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
    out = f"site/img/{name}.jpg"
    im.save(out, quality=90, optimize=True, progressive=True)
    print(f"{name:13s} {im.width}x{im.height}  {os.path.getsize(out)//1024}KB")
