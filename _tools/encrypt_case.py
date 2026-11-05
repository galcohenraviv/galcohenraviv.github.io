import base64, glob, os, sys
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Encrypt a password-protected case study for the static site.
#   python encrypt_case.py <case.html> <image dir> <out dir> <password> <salt file>
# Output (all text, base64): <out>/case.txt = "v1:<salt>:<iterations>\n<iv+ciphertext>", and <out>/<image>.txt per image.
# Cases sharing a salt file share one key, so one password unlocks them all in the browser
# (WebCrypto: PBKDF2-SHA256 -> AES-256-GCM).
html_path, img_dir, out_dir, password, salt_path = sys.argv[1:6]
ITER = 310_000

if not os.path.exists(salt_path):
    with open(salt_path, "wb") as f:
        f.write(os.urandom(16))
salt = open(salt_path, "rb").read()
key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITER).derive(password.encode("utf-8"))
aes = AESGCM(key)

def seal(data: bytes) -> str:
    iv = os.urandom(12)
    return base64.b64encode(iv + aes.encrypt(iv, data, None)).decode("ascii")

os.makedirs(out_dir, exist_ok=True)
for old in glob.glob(os.path.join(out_dir, "*.txt")):
    os.remove(old)

html = open(html_path, encoding="utf-8").read().encode("utf-8")
with open(os.path.join(out_dir, "case.txt"), "w", encoding="ascii") as f:
    f.write(f"v1:{base64.b64encode(salt).decode()}:{ITER}\n{seal(html)}")

names = []
for img in sorted(glob.glob(os.path.join(img_dir, "*.webp")) + glob.glob(os.path.join(img_dir, "*.png"))):
    name = os.path.splitext(os.path.basename(img))[0]
    with open(os.path.join(out_dir, name + ".txt"), "w", encoding="ascii") as f:
        f.write(seal(open(img, "rb").read()))
    names.append(name)

refs = {r.split('"')[0] for r in html.decode().split('data-enc="')[1:]}
missing = refs - set(names)
assert not missing, f"images referenced but not found: {missing}"
print(f"encrypted case + {len(names)} images -> {out_dir}")
