import os, sys, glob, pymupdf

# Contact sheet of all jpgs in a folder, labelled, for a quick visual check.
src, out = sys.argv[1], sys.argv[2]
files = sorted(glob.glob(os.path.join(src, "*.jpg")))
cols, cw, ch = 7, 200, 230
rows = (len(files) + cols - 1) // cols
doc = pymupdf.open()
page = doc.new_page(width=cols * cw, height=rows * ch)
for i, f in enumerate(files):
    x, y = (i % cols) * cw, (i // cols) * ch
    page.insert_image(pymupdf.Rect(x + 5, y + 5, x + cw - 5, y + ch - 25), filename=f, keep_proportion=True)
    page.insert_text((x + 6, y + ch - 10), os.path.basename(f)[:-4], fontsize=11)
page.get_pixmap().save(out)
