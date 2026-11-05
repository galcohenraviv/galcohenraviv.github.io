import sys

# Put back the hero dot-grid canvas (markup, styles, theme hook) and drop the flip-letter styles.
path = sys.argv[1]
s = open(path, encoding="utf-8").read()
a = s.index("/* flip letters:")
b = s.index(".hero .lede {", a)
s = s[:a] + s[b:]
for old, new in [
    ('.hero .wrap { position: relative;', '.hero canvas { position: absolute; inset: 0; width: 100%; height: 100%; pointer-events: none; }\n.hero .wrap { position: relative;'),
    ('.hero > .wrap { animation', '.hero > .wrap, .hero canvas { animation'),
    ('  <section class="hero" id="top">\n', '  <section class="hero" id="top">\n    <canvas id="gaze" aria-hidden="true"></canvas>\n'),
    ("    store.set('theme', next);\n", "    store.set('theme', next);\n    readColors();\n"),
]:
    assert s.count(old) == 1, old
    s = s.replace(old, new)
assert ".fl " not in s and "flip" not in s.split("<script>")[0]
open(path, "w", encoding="utf-8").write(s)
print("ok")
