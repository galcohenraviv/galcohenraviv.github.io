import sys

# Remove the "How I work" section and the hero dot-grid canvas from site/index.html, by marker.
path = sys.argv[1]
s = open(path, encoding="utf-8").read()

def cut(s, start, end, repl=""):
    a = s.index(start)
    b = s.index(end, a)
    return s[:a] + repl + s[b:]

s = cut(s, '  <section class="how" id="how"', '  <section class="block" id="about">')
s = cut(s, '/* ---------- how I work', '/* ---------- about ---------- */')
s = cut(s, '  /* ---------- how I work: pinned', '  /* ---------- scroll delights')
s = cut(s, '  /* ---------- hero: dot grid', '})();', '  /*HERO_JS*/\n')
for old, new in [
    ('    <canvas id="gaze" aria-hidden="true"></canvas>\n', ''),
    ('.hero canvas { position: absolute; inset: 0; width: 100%; height: 100%; pointer-events: none; }\n', ''),
    ('.hero > .wrap, .hero canvas { animation', '.hero > .wrap { animation'),
    ('    store.set(\'theme\', next);\n    readColors();\n', '    store.set(\'theme\', next);\n'),
]:
    assert s.count(old) == 1, old
    s = s.replace(old, new)
assert 'readColors' not in s and 'gaze"' not in s and 'how-' not in s
open(path, "w", encoding="utf-8").write(s)
print("ok")
