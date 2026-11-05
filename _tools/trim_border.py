import sys, pymupdf

# Report and trim dark border bands from screenshot exports (frame edges/shadows baked into the PNG).
# python trim_border.py <in.png> <out.png>
src, out = sys.argv[1], sys.argv[2]
pix = pymupdf.Pixmap(src)
if pix.alpha:
    pix = pymupdf.Pixmap(pix, 0)
w, h = pix.width, pix.height

def dark(x, y):
    r, g, b = pix.pixel(x, y)[:3]
    return (r + g + b) / 3 < 120

def col_dark(x):
    return sum(dark(x, y) for y in range(0, h, 7)) > 0.6 * (h / 7)

def row_dark(y):
    return sum(dark(x, y) for x in range(0, w, 7)) > 0.6 * (w / 7)

left = 0
while left < w // 4 and col_dark(left): left += 1
right = w - 1
while right > w * 3 // 4 and col_dark(right): right -= 1
top = 0
while top < h // 4 and row_dark(top): top += 1
bottom = h - 1
while bottom > h * 3 // 4 and row_dark(bottom): bottom -= 1
# take a few extra pixels to drop anti-aliased edge
pad = 2 if (left or top or w - 1 - right or h - 1 - bottom) else 0
box = pymupdf.IRect(left + pad, top + pad, right + 1 - pad, bottom + 1 - pad)
print(f"{src}: {w}x{h} -> trim L{left} T{top} R{w-1-right} B{h-1-bottom} -> {box.width}x{box.height}")
doc = pymupdf.open()
page = doc.new_page(width=box.width, height=box.height)
page.insert_image(page.rect, pixmap=pix, clip=box) if False else None
cropped = pymupdf.Pixmap(pix.colorspace, box, False)
cropped.copy(pix, box)
cropped.set_origin(0, 0)
cropped.save(out)
