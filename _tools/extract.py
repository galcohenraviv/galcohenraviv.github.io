import sys, os, pymupdf

src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
doc = pymupdf.open(src)
with open(os.path.join(out, "text.txt"), "w", encoding="utf-8") as f:
    for i, page in enumerate(doc):
        f.write(f"\n===== PAGE {i+1} ({page.rect.width:.0f}x{page.rect.height:.0f}) =====\n")
        f.write(page.get_text())
        z = 1000 / page.rect.width
        page.get_pixmap(matrix=pymupdf.Matrix(z, z)).save(os.path.join(out, f"p{i+1:02d}.png"))
print(src, len(doc), "pages")
