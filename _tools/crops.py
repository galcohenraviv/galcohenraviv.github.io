import os, sys, pymupdf

# Crop regions (PDF points: x0, y0, x1, y1) from each case-study PDF into site images.
D = sys.argv[1]
OUT = sys.argv[2]

CROPS = {
    "VoiceMind.pdf": {
        "vm-dashboard":  (238, 6982, 1682, 8491),
        "vm-cover":      (240, 6984, 1680, 8064),
        "vm-topics":     (238, 8856, 1682, 9652),
        "vm-automation": (238, 9996, 1682, 11026),
        "vm-step1":      (238, 11451, 1682, 12582),
        "vm-step2":      (238, 12656, 1682, 13956),
        "vm-step3":      (238, 14032, 1682, 15474),
        "vm-agents":     (238, 15788, 1682, 16784),
        "vm-call":       (238, 17093, 1682, 18690),
    },
    "CAL app case study.pdf": {
        "cal-screens":   (1020, 1485, 1675, 1970),
        "cal-lab":       (960, 2547, 1600, 2907),
        "cal-heatstrip": (0, 5230, 1920, 5690),
        "cal-cards":     (1073, 6928, 1778, 7348),
        "cal-keyboard":  (285, 8028, 810, 8452),
        "cal-almost":    (1120, 8760, 1580, 9275),
        "cal-multicard": (1225, 9590, 1505, 10565),
        "cal-gaze":      (1050, 11060, 1660, 12100),
    },
    "Bank Hapoalim loan case study.pdf": {
        "bh-old":        (40, 1690, 1880, 2650),
        "bh-sketches":   (70, 6575, 1850, 7140),
        "bh-purpose":    (778, 7615, 1142, 8385),
        "bh-offer":      (778, 8640, 1142, 9680),
        "bh-loader":     (778, 9930, 1142, 10595),
        "bh-confirm":    (778, 10850, 1142, 11855),
        "bh-approved":   (0, 12060, 1145, 12850),
        "bh-upsell":     (778, 13130, 1142, 13945),
    },
}

os.makedirs(OUT, exist_ok=True)
for pdf, crops in CROPS.items():
    page = pymupdf.open(os.path.join(D, pdf))[0]
    for name, box in crops.items():
        clip = pymupdf.Rect(*box)
        # high-res: ~2600px for wide frames, ~3.2x for phone-width crops
        z = min(3.2, 2600 / clip.width)
        pix = page.get_pixmap(matrix=pymupdf.Matrix(z, z), clip=clip)
        path = os.path.join(OUT, name + ".jpg")
        pix.save(path, jpg_quality=90)
        print(f"{name:14s} {pix.width}x{pix.height}  {os.path.getsize(path)//1024}KB")

