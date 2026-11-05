import sys, pymupdf

# List embedded image placements and large drawn rectangles, to locate crop regions.
page = pymupdf.open(sys.argv[1])[0]
print("== images")
for info in page.get_image_info():
    b = pymupdf.Rect(info["bbox"])
    if b.width > 120 and b.height > 120:
        print(f"img  x{b.x0:6.0f}-{b.x1:6.0f}  y{b.y0:7.0f}-{b.y1:7.0f}  ({b.width:.0f}x{b.height:.0f})")
print("== big rects")
seen = set()
for d in page.get_drawings():
    r = d["rect"]
    if r.width > 700 and r.height > 400:
        key = (round(r.x0), round(r.y0), round(r.x1), round(r.y1))
        if key not in seen:
            seen.add(key)
            print(f"rect x{r.x0:6.0f}-{r.x1:6.0f}  y{r.y0:7.0f}-{r.y1:7.0f}  ({r.width:.0f}x{r.height:.0f})")
