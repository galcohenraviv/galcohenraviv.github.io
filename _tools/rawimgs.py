import os, sys, pymupdf

# Save embedded raster images whose placement falls inside a region (PDF points), at native resolution.
src, out, y0, y1 = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
os.makedirs(out, exist_ok=True)
doc = pymupdf.open(src)
page = doc[0]
for info in page.get_image_info(xrefs=True):
    b = pymupdf.Rect(info["bbox"])
    if info["xref"] and b.y0 >= y0 and b.y1 <= y1:
        pix = pymupdf.Pixmap(doc, info["xref"])
        if pix.alpha or pix.n > 3:
            pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
        name = f"x{info['xref']}_{int(b.x0)}_{int(b.y0)}.png"
        pix.save(os.path.join(out, name))
        print(name, pix.width, pix.height, "placed", f"{b.width:.0f}x{b.height:.0f}")
