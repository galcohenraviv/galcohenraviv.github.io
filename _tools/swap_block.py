import sys

# Replace one marked script block in site/index.html: the block runs from its start marker up to (not including) the end marker.
path, start, end, repl_file = sys.argv[1:5]
s = open(path, encoding="utf-8").read()
a = s.index(start)
b = s.index(end, a)
s = s[:a] + open(repl_file, encoding="utf-8").read() + s[b:]
open(path, "w", encoding="utf-8").write(s)
print("ok")
