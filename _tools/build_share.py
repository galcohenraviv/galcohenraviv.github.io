"""Build one self-contained HTML file of the portfolio for sharing as a file.

Inlines every img/ image as a data URI and embeds the encrypted Fireblocks
case files (lm/, sw/, er/), so the page works offline when opened from disk.
Only already-encrypted content is embedded; _private/ is never read.

Run from the Portfolio folder:  python -I _tools/build_share.py
Output: share/gal-cohen-raviv-portfolio.html
"""
import base64
import json
import os
import re

SITE = 'site'
OUT = 'share/gal-cohen-raviv-portfolio.html'
MIME = {'jpg': 'jpeg', 'jpeg': 'jpeg', 'png': 'png', 'webp': 'webp', 'svg': 'svg+xml', 'gif': 'gif'}

s = open(f'{SITE}/index.html', encoding='utf-8').read()


def datauri(m):
    path = m.group(1).split('?')[0]
    ext = path.rsplit('.', 1)[1].lower()
    data = base64.b64encode(open(f'{SITE}/{path}', 'rb').read()).decode()
    return f'src="data:image/{MIME[ext]};base64,{data}"'


s, n = re.subn(r'src="(img/[^"]+)"', datauri, s)

enc = {}
for d in ('lm', 'sw', 'er'):
    for f in os.listdir(f'{SITE}/{d}'):
        enc[f'{d}/{f}'] = open(f'{SITE}/{d}/{f}', encoding='utf-8').read()

swaps = [
    ('(await (await fetch(`${dir}/case.txt`)).text())', '(__ENC[`${dir}/case.txt`])'),
    ('b64(await (await fetch(`${dir}/${img.dataset.enc}.txt`)).text())', 'b64(__ENC[`${dir}/${img.dataset.enc}.txt`])'),
]
for old, new in swaps:
    assert s.count(old) == 1, old
    s = s.replace(old, new)

blob = '<script>window.__ENC=' + json.dumps(enc).replace('</', '<\\/') + ';</script>\n'
i = s.index('<script')
s = s[:i] + blob + s[i:]

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, 'w', encoding='utf-8').write(s)
print(f'{n} images inlined, {len(enc)} encrypted files embedded, {os.path.getsize(OUT) // 1048576} MB -> {OUT}')
