import sys

# Replace the home-page preview images with layered "pv" compositions (markup + styles + parallax script).
path = sys.argv[1]
s = open(path, encoding="utf-8").read()

def rep(old, new):
    global s
    assert s.count(old) == 1, ("not unique/missing", old[:80])
    s = s.replace(old, new)

def win(src, alt, w, h, style, d):
    return (f'<div class="pv-l pv-win" style="{style};--d:{d}"><i class="pv-bar" aria-hidden="true"></i>'
            f'<img src="img/{src}" alt="{alt}" width="{w}" height="{h}" loading="lazy"></div>')

def card(src, alt, w, h, style, d, r=0):
    return (f'<div class="pv-l pv-card" style="{style};--d:{d};--r:{r}deg">'
            f'<img src="img/{src}" alt="{alt}" width="{w}" height="{h}" loading="lazy"></div>')

def phone(src, alt, w, h, style, d, r=0):
    return (f'<div class="pv-l pv-phone" style="{style};--d:{d};--r:{r}deg">'
            f'<img src="img/{src}" alt="{alt}" width="{w}" height="{h}" loading="lazy"></div>')

def chip(text, style, d=10):
    return f'<span class="pv-l pv-chip" style="{style};--d:{d}">{text}</span>'

def pv(hue, *layers):
    return f'<div class="pv" style="--hue:{hue}">' + "".join(layers) + "</div>"

LM = pv("#d9a43b",
        win("pv-lm-base.jpg", "Trading view with live bid and ask quotes per provider", 1400, 630, "left:9%;top:17%;width:112%", -6),
        card("pv-lm-float.jpg", "Locked quote card ready to execute a sell", 470, 274, "left:5%;top:47%;width:46%", 18, -2),
        chip("Live quotes", "left:5%;top:6%"))
SW = pv("#4f7cff",
        win("pv-sw-base.jpg", "Create swap order with suggested pairs and available offers", 960, 689, "left:26%;top:12%;width:86%", -6),
        card("pv-sw-float.jpg", "Best offer expanded with slippage, fees and total after fees", 272, 290, "left:5%;top:34%;width:36%", 18, 2),
        chip("Best rate, every route", "left:5%;top:6%"))
ER = pv("#7c6af2",
        win("pv-er-base.jpg", "Earn opportunities compared by asset, protocol, liquidity and APY", 1400, 632, "left:6%;top:17%;width:112%", -6),
        card("pv-er-float.jpg", "Deposit summary panel with APY, exposure and the approval flow", 620, 865, "right:6%;top:24%;width:31%", 18, 2),
        chip("Aave · Morpho", "left:6%;top:6%"))
VM = pv("#6d5cf0",
        win("pv-vm-base.jpg", "VoiceMind customer insights dashboard", 1600, 1200, "left:9%;top:13%;width:104%", -6),
        card("pv-vm-float.jpg", "Suggested auto-response with 94% confidence", 887, 411, "left:4%;bottom:8%;width:60%", 18, -1.5),
        chip("94% confidence", "left:5%;top:5%"))
CAL = pv("#2f9bf0",
         phone("cal-phone.jpg", "CAL app dashboard with card balance and monthly charges", 321, 936, "left:17%;top:13%;width:29%", -5),
         card("pv-cal-float.jpg", "Eye-tracking heatmap on the card selection screen", 520, 922, "left:53%;top:20%;width:28%", 16, 4),
         chip("15 participants", "left:5%;top:5%"))
BH = pv("#e0483e",
        phone("bh-purpose.jpg", "Choose loan purpose screen", 1166, 2464, "left:9%;top:20%;width:26%", 6, -3),
        phone("bh-offer.jpg", "Best offer screen", 1166, 3328, "left:37%;top:10%;width:26%", -6),
        phone("bh-upsell.jpg", "Money transferred confirmation with an additional loan offer", 1166, 2608, "left:65%;top:22%;width:26%", 12, 3),
        chip("Personalized by purpose", "left:5%;top:5%"))

rep('<div class="motif"><img src="img/fb-liquidity.png" alt="USDC/USD quotes from three liquidity providers with best bid and ask" width="546" height="381"></div>',
    f'<div class="motif">{LM}</div>')
rep('<div class="motif"><img src="img/fb-swap.png" alt="Create swap order dialog: same-chain swap from USDC to USDT via Uniswap" width="436" height="393"></div>',
    f'<div class="motif">{SW}</div>')
rep('<div class="motif"><img src="img/fb-earn.jpg" alt="Earn opportunities: lending vaults and markets with their asset and protocol" width="901" height="537"></div>',
    f'<div class="motif">{ER}</div>')
rep('<div class="shot tilt"><img src="img/vm-cover.jpg" alt="VoiceMind customer insights dashboard with sentiment KPIs and sentiment over time" loading="lazy" width="2601" height="1950"></div>',
    f'<div class="shot">{VM}</div>')
rep('<div class="shot tilt stage stage-cal"><img src="img/cal-phone.jpg" alt="CAL app dashboard with card balance and monthly charges" loading="lazy" width="321" height="936"></div>',
    f'<div class="shot">{CAL}</div>')
rep('<div class="shot tilt stage"><img src="img/bh-purpose.jpg" alt="Choose loan purpose screen" loading="lazy" width="1166" height="2464"><img src="img/bh-offer.jpg" alt="Best offer screen" loading="lazy" width="1166" height="3328"><img src="img/bh-upsell.jpg" alt="Money transferred confirmation with additional loan offer" loading="lazy" width="1166" height="2608"></div>',
    f'<div class="shot">{BH}</div>')

# --- styles: drop the old single-image preview rules, add the layered system
rep(""".priv .motif { aspect-ratio: 4 / 3; max-width: 100%; overflow: hidden; border-bottom: 1px solid var(--line); background: #e9ebf0; }
.priv .motif img { width: 100%; height: 100%; object-fit: cover; transition: transform 1s var(--ease); }
.priv:hover .motif img { transform: scale(1.04); }""",
""".priv .motif { position: relative; aspect-ratio: 4 / 3; max-width: 100%; overflow: hidden; border-bottom: 1px solid var(--line); }""")

a = s.index(".shot img { width: 100%; height: 100%; object-fit: cover;")
b = s.index(".case-row:hover .shot { box-shadow:", a)
s = s[:a] + s[b:]
rep(".case-row:hover .shot img { transform: scale(1.025); }\n", "")
rep("""    .shot:not(.stage) img { height: 112%; animation: drift linear both; animation-timeline: view(); animation-range: cover 0% cover 100%; }""",
    """    .pv-card, .pv-phone { animation: pv-in linear both; animation-timeline: view(); animation-range: entry 5% cover 35%; }""")
a = s.index("    /* phones rise from the panel edge, staggered */")
b = s.index("\n\n", a)
s = s[:a] + s[b + 1:]
rep("@keyframes drift { from { translate: 0 0; } to { translate: 0 -10.7%; } }\n@keyframes phone-up { from { translate: 0 35%; } }\n",
    "@keyframes pv-in { from { opacity: 0; scale: .92; } }\n")

PV_CSS = """
/* ---------- layered previews: tinted stage, framed main screen, floating UI detail, parallax depth ---------- */
.shot { position: relative; }
.pv {
  position: absolute; inset: 0; overflow: hidden; isolation: isolate; --mx: 0; --my: 0;
  background:
    radial-gradient(75% 65% at 88% -5%, color-mix(in oklab, var(--hue) 38%, transparent), transparent 70%),
    radial-gradient(60% 60% at -5% 105%, color-mix(in oklab, var(--hue) 22%, transparent), transparent 70%),
    color-mix(in oklab, var(--hue) 9%, var(--paper-2));
}
.pv::before {
  content: ""; position: absolute; inset: 0; z-index: -1; pointer-events: none;
  background-image:
    linear-gradient(color-mix(in oklab, var(--ink) 6%, transparent) 1px, transparent 1px),
    linear-gradient(90deg, color-mix(in oklab, var(--ink) 6%, transparent) 1px, transparent 1px);
  background-size: 22px 22px;
  -webkit-mask-image: radial-gradient(80% 80% at 70% 20%, #000 0%, transparent 75%);
  mask-image: radial-gradient(80% 80% at 70% 20%, #000 0%, transparent 75%);
}
.pv::after {
  content: ""; position: absolute; inset: -30%; z-index: 5; pointer-events: none;
  background: linear-gradient(115deg, transparent 42%, rgba(255, 255, 255, .28) 50%, transparent 58%);
  transform: translateX(-70%); transition: transform 1.3s var(--ease);
}
a:hover .pv::after { transform: translateX(70%); }
.pv-l {
  position: absolute;
  translate: calc(var(--mx) * var(--d, 0) * 1px) calc(var(--my) * var(--d, 0) * 1px);
  transform: rotate(var(--r, 0deg));
  transition: translate .8s var(--ease), transform .8s var(--ease), box-shadow .8s var(--ease);
}
.pv-l img { display: block; width: 100%; height: auto; }
.pv-win {
  border-radius: 10px; overflow: hidden; background: #fff; z-index: 1;
  box-shadow: 0 0 0 1px rgba(20, 24, 33, .08), 0 2px 4px rgba(20, 24, 33, .04), 0 28px 56px -24px rgba(20, 24, 40, .38);
}
.pv-bar {
  display: block; height: 15px; border-bottom: 1px solid #e8eaef;
  background:
    radial-gradient(circle at 10px 50%, #ff6159 3px, transparent 3.5px),
    radial-gradient(circle at 21px 50%, #ffbd2e 3px, transparent 3.5px),
    radial-gradient(circle at 32px 50%, #28c840 3px, transparent 3.5px),
    #f5f6f8;
}
.pv-card {
  border-radius: 10px; overflow: hidden; background: #fff; z-index: 2;
  box-shadow: 0 0 0 1px rgba(20, 24, 33, .08), 0 10px 20px -10px rgba(20, 24, 40, .25), 0 36px 70px -20px rgba(20, 24, 40, .45);
}
.pv-phone {
  aspect-ratio: 9 / 19.5; padding: 4px; border-radius: 22px; background: #101217; z-index: 1;
  box-shadow: 0 0 0 1px rgba(255, 255, 255, .06) inset, 0 30px 60px -22px rgba(15, 18, 30, .55);
}
.pv-phone img { height: 100%; object-fit: cover; object-position: top; border-radius: 18px; }
.pv-chip {
  z-index: 4; display: inline-flex; align-items: center; gap: 7px; white-space: nowrap;
  font-family: var(--f-mono); font-size: .7rem; letter-spacing: .01em; color: var(--ink);
  padding: 5px 11px; border-radius: 999px;
  background: color-mix(in oklab, var(--paper) 72%, transparent);
  border: 1px solid color-mix(in oklab, var(--ink) 10%, transparent);
  -webkit-backdrop-filter: blur(10px) saturate(1.4); backdrop-filter: blur(10px) saturate(1.4);
}
.pv-chip::before { content: ""; width: 6px; height: 6px; border-radius: 50%; background: var(--hue); box-shadow: 0 0 0 3px color-mix(in oklab, var(--hue) 25%, transparent); }
a:hover .pv-win { transform: rotate(var(--r, 0deg)) translateY(-3px); }
a:hover .pv-card { transform: rotate(var(--r, 0deg)) translateY(-10px) scale(1.035); box-shadow: 0 0 0 1px rgba(20, 24, 33, .08), 0 14px 28px -12px rgba(20, 24, 40, .28), 0 50px 90px -24px rgba(20, 24, 40, .5); }
a:hover .pv-phone { transform: rotate(var(--r, 0deg)) translateY(-8px); }
@media (max-width: 520px) { .pv-chip { font-size: .62rem; padding: 4px 9px; } .pv-bar { height: 11px; background-size: auto; } }
"""
rep("/* ---------- about ---------- */", PV_CSS + "\n/* ---------- about ---------- */")

PV_JS = """  /* ---------- previews: layers drift with the cursor at different depths ---------- */
  if (fine && !reduce) {
    document.querySelectorAll('.pv').forEach(pv => {
      const host = pv.closest('a') || pv;
      host.addEventListener('pointermove', e => {
        const r = pv.getBoundingClientRect();
        pv.style.setProperty('--mx', (((e.clientX - r.left) / r.width - .5) * 2).toFixed(3));
        pv.style.setProperty('--my', (((e.clientY - r.top) / r.height - .5) * 2).toFixed(3));
      });
      host.addEventListener('pointerleave', () => { pv.style.setProperty('--mx', 0); pv.style.setProperty('--my', 0); });
    });
  }

"""
rep("  /* ---------- hero: dot grid", PV_JS + "  /* ---------- hero: dot grid")

open(path, "w", encoding="utf-8").write(s)
print("ok")
