import sys

# Reorder the case-study sections in a fragment by their label text: python reorder.py file "Label A" "Label B" ...
path, order = sys.argv[1], sys.argv[2:]
s = open(path, encoding="utf-8").read()
marker = '  <section class="cs-sec">'
head, *parts = s.split(marker)
last_end = parts[-1].index("</section>") + len("</section>\n")
tail = parts[-1][last_end:]
parts[-1] = parts[-1][:last_end]

def label(p):
    return p.split('<span class="label">', 1)[1].split("<", 1)[0]

by_label = {label(p): p for p in parts}
assert sorted(by_label) == sorted(order), (list(by_label), order)
open(path, "w", encoding="utf-8").write(head + "".join(marker + by_label[k] for k in order) + tail)
print(" > ".join(order))
