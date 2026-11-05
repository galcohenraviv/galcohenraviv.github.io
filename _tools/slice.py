import sys, os, pymupdf

# Render a tall single-page PDF into horizontal slices (PDF-point heights) for previewing.
src, out, step = sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 1600
os.makedirs(out, exist_ok=True)
page = pymupdf.open(src)[0]
w, h = page.rect.width, page.rect.height
z = 900 / w
y, i = 0, 0
while y < h:
    clip = pymupdf.Rect(0, y, w, min(y + step, h))
    page.get_pixmap(matrix=pymupdf.Matrix(z, z), clip=clip).save(os.path.join(out, f"s{i:02d}.png"))
    y += step
    i += 1
print(out, i, "slices")
