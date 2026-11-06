"""One-off patch: shared Figma-style cursor chip with a smart-animate morph, used by the hero and the hover labels."""
p = 'site/index.html'
s = open(p, encoding='utf-8').read()


def rep(old, new):
    global s
    assert s.count(old) == 1, (s.count(old), old[:80])
    s = s.replace(old, new)


# ---- CSS: shared chip
a = s.index('.chip { position: absolute; left: 0; top: 0; will-change: transform; }')
b = s.index('@media (prefers-reduced-motion: reduce) {\n  .cc-title .caret', a)
s = s[:a] + '''/* Figma-style cursor chip (hero + hover labels): a coloured arrow plus a pill. Colour, width and text morph
   between states ("smart animate"); --c is the multiplayer colour. */
.chip { position: absolute; left: 0; top: 0; will-change: transform; }
.chip svg { position: absolute; left: -2px; top: -2px; width: 20px; height: 22px; overflow: visible;
  filter: drop-shadow(0 1px 1.5px rgba(0,0,0,.25)); }
.chip svg path { fill: var(--c); transition: fill .42s cubic-bezier(.2,.9,.25,1); }
.chip .lbl {
  position: absolute; left: 15px; top: 17px; display: block; overflow: hidden; white-space: nowrap;
  font: 500 .875rem/1 var(--f-sans); letter-spacing: -0.005em; padding: 7px 11px 8px;
  border-radius: 3px 12px 12px 12px; color: #fff; background: var(--c); transform-origin: 0 0;
  box-shadow: 0 1px 2px rgba(0,0,0,.12), 0 6px 16px -6px color-mix(in oklab, var(--c) 70%, transparent);
  transition: background-color .42s cubic-bezier(.2,.9,.25,1), color .42s, box-shadow .42s;
}
.chip .txt { display: inline-block; }
.chip .txt.leaving { position: absolute; left: 11px; top: 7px; }
.chip.dark-ink .lbl { color: #1c1b19; }
.chip.out > * { animation: chip-out .55s ease forwards; transform-origin: 0 0; }
@keyframes chip-out { to { opacity: 0; filter: blur(3px); transform: scale(.92); } }
.cursor-chip { position: fixed; z-index: 50; pointer-events: none; opacity: 0; transform: translate3d(-200px, -200px, 0); transition: opacity .18s; }
.cursor-chip.on { opacity: 1; }
.chip-cursor [data-cursor], .chip-cursor [data-cursor] * { cursor: none; }
''' + s[b:]
rep('''  .chip span { animation: none; }
  .chip.out { animation: chip-fade .4s ease forwards; }''', '''  .chip.out > * { animation: chip-fade .4s ease forwards; }''')

# old pill cursor CSS
a = s.index('/* cursor label (fine pointers only) */')
b = s.index('.cursor .dot {', a)
b = s.index('\n', b) + 1
s = s[:a] + s[b:]

# ---- markup
rep('<div class="cursor" id="cursor" aria-hidden="true"><span class="dot"></span><span id="cursorText"></span></div>',
    '<div class="chip cursor-chip" id="cursor" aria-hidden="true"></div>')

# ---- shared JS helpers, defined before the hover cursor uses them
rep("  const cursor = document.getElementById('cursor');\n", '''  /* ---------- Figma-style cursor chip, shared by the hero and the hover labels ---------- */
  const CHIP_COLORS = [['#9747FF'], ['#0C8CE9'], ['#0E9F98'], ['#F2545B'], ['#FFB224', 1], ['#14AE5C']];   // Figma multiplayer palette; amber takes dark ink
  const SMART = 'cubic-bezier(.2,.9,.25,1)';
  const fillChip = el => { el.innerHTML = '<svg viewBox="0 0 20 22" aria-hidden="true"><path d="M2 2 L2 18.5 L6.6 14.2 L9.6 20.6 L12.6 19.2 L9.7 12.9 L16 12.9 Z" stroke="#fff" stroke-width="1.4" stroke-linejoin="round"/></svg><span class="lbl"><span class="txt"></span></span>'; return el; };
  const paintChip = (el, i) => { const [c, dark] = CHIP_COLORS[i % CHIP_COLORS.length]; el.style.setProperty('--c', c); el.classList.toggle('dark-ink', !!dark); };
  const setChipText = (el, text) => { const t = document.createElement('span'); t.className = 'txt'; t.textContent = text; el.querySelector('.lbl').replaceChildren(t); };
  const popChip = el => { if (!reduce) el.querySelector('.lbl').animate([{ opacity: 0, transform: 'scale(.55)' }, { opacity: 1, transform: 'none' }], { duration: 380, easing: 'cubic-bezier(.34,1.56,.64,1)' }); };
  // smart animate: the pill eases to the new width while the old words slide up and out and the new ones slide in
  const morphChip = (el, text) => {
    const lbl = el.querySelector('.lbl'), cur = lbl.querySelector('.txt:not(.leaving)');
    if (cur && cur.textContent === text) return;
    if (reduce || !cur || !cur.textContent) return setChipText(el, text);
    lbl.querySelectorAll('.leaving').forEach(n => n.remove());
    const w0 = lbl.offsetWidth;
    cur.classList.add('leaving');
    const nu = document.createElement('span'); nu.className = 'txt'; nu.textContent = text;
    lbl.append(nu);
    lbl.animate([{ width: w0 + 'px' }, { width: lbl.offsetWidth + 'px' }], { duration: 420, easing: SMART });
    cur.animate([{ opacity: 1, transform: 'none', filter: 'blur(0)' }, { opacity: 0, transform: 'translateY(-110%)', filter: 'blur(2px)' }],
      { duration: 260, easing: 'cubic-bezier(.4,0,.6,1)', fill: 'forwards' }).onfinish = () => cur.remove();
    nu.animate([{ opacity: 0, transform: 'translateY(110%)', filter: 'blur(2px)' }, { opacity: 1, transform: 'none', filter: 'blur(0)' }],
      { duration: 420, easing: SMART });
  };

  const cursor = fillChip(document.getElementById('cursor'));
''')

# ---- hover cursor logic
a = s.index("  const cursorText = document.getElementById('cursorText');")
b = s.index("    document.addEventListener('pointerleave', hideCursor);", a)
s = s[:a] + '''  let tx = -200, ty = -200, raf = 0, hoverColor = Math.floor(Math.random() * CHIP_COLORS.length), hiddenAt = 0;
  if (fine && !reduce) {
    root.classList.add('chip-cursor');                // the chip's arrow stands in for the system cursor over labelled targets
    const place = () => { raf = 0; cursor.style.transform = `translate3d(${tx}px, ${ty}px, 0)`; };
    addEventListener('pointermove', e => {
      tx = e.clientX; ty = e.clientY;
      const el = e.target.closest('[data-cursor]');
      if (el !== active) {
        active = el;
        if (el) {
          paintChip(cursor, ++hoverColor);
          // moving straight from one target to the next morphs the chip; arriving fresh pops it in
          if (performance.now() - hiddenAt < 300 && cursor.querySelector('.txt').textContent) morphChip(cursor, el.dataset.cursor);
          else { setChipText(cursor, el.dataset.cursor); popChip(cursor); }
          cursor.classList.add('on');
        } else { cursor.classList.remove('on'); hiddenAt = performance.now(); }
      }
      if (!raf) raf = requestAnimationFrame(place);
    }, { passive: true });
''' + s[b:]

# ---- hero: one persistent chip that morphs between keywords
a = s.index('  /* ---------- hero: Figma-style multiplayer cursor chips ---------- */')
b = s.index("    addEventListener('hashchange', () => { clearTimeout(idleT); goIdle(); });\n  })();", a)
b = s.index('  })();', b) + len('  })();')
s = s[:a] + '''  /* ---------- hero: Figma-style multiplayer cursor chip that smart-animates between keywords ---------- */
  (() => {
    const hero = document.getElementById('top'), layer = document.getElementById('chips');
    if (!hero || !layer) return;
    const WORDS = ['Product Design', 'Design Systems', 'AI-First UI', 'Claude Code', 'Figma', 'Fintech', 'Crypto',
      'Cybersecurity', 'Banking', 'Payments', 'B2B SaaS', 'B2C Apps', 'Front-end', 'Prototyping', 'Web3', 'Micro-interactions'];
    const SPAWN_DIST = 40, SPAWN_GAP = 1000, IDLE = 2000;
    let bag = [], lastWord = '', colorAt = Math.floor(Math.random() * CHIP_COLORS.length);
    const nextWord = () => {
      if (!bag.length) { bag = WORDS.slice().sort(() => Math.random() - .5); if (bag[0] === lastWord) bag.push(bag.shift()); }
      return (lastWord = bag.shift());
    };
    let chip = null, idleT = 0, lastX = 0, lastY = 0, lastSpawn = -Infinity, px = 0, py = 0, raf = 0;
    const place = () => { raf = 0; if (chip) chip.style.transform = `translate3d(${px}px, ${py}px, 0)`; };
    const next = () => { paintChip(chip, ++colorAt); lastX = px; lastY = py; lastSpawn = performance.now(); };
    const appear = () => {
      layer.replaceChildren();
      chip = fillChip(document.createElement('div')); chip.className = 'chip';
      next(); setChipText(chip, nextWord()); place();
      layer.append(chip); popChip(chip);
      hero.classList.add('chipping');
    };
    const goIdle = () => {
      if (!chip) return;
      const old = chip; chip = null;
      old.classList.add('out'); setTimeout(() => old.remove(), 600);
      hero.classList.remove('chipping');
    };
    const onMove = e => {
      const r = hero.getBoundingClientRect();
      px = e.clientX - r.left; py = e.clientY - r.top;
      if (!chip) appear();
      else if (Math.hypot(px - lastX, py - lastY) >= SPAWN_DIST && performance.now() - lastSpawn >= SPAWN_GAP) { next(); morphChip(chip, nextWord()); }
      if (!raf) raf = requestAnimationFrame(place);
      clearTimeout(idleT); idleT = setTimeout(goIdle, IDLE);
    };
    hero.addEventListener('pointermove', onMove, { passive: true });
    hero.addEventListener('pointerdown', onMove, { passive: true });
    hero.addEventListener('pointerleave', () => { clearTimeout(idleT); goIdle(); });
    addEventListener('hashchange', () => { clearTimeout(idleT); goIdle(); });
  })();''' + s[b:]

for w in ('cursorText', '.cursor .dot', '.cursor {', 'COLORS[', 'retire(', 'cx + 16'):
    print(w, s.count(w))
open(p, 'w', encoding='utf-8').write(s)
