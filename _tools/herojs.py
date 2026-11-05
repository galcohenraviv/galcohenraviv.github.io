import sys

# Replace the hero headline script block (between its marker and the closing IIFE) with the code in a file.
path, js = sys.argv[1], open(sys.argv[2], encoding="utf-8").read()
s = open(path, encoding="utf-8").read()
start = s.index("  /* ---------- hero:")
end = s.index("})();", start)
s = s[:start] + js + s[end:]
open(path, "w", encoding="utf-8").write(s)
print("ok")
