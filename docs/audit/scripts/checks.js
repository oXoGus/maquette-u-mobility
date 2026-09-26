() => {
  const vw = window.innerWidth, vh = window.innerHeight;
  const mobile = vw <= 900;
  const out = { vw, vh, docScrollW: document.documentElement.scrollWidth, bodyScrollW: document.body.scrollWidth };
  out.hOverflow = out.docScrollW > vw;
  const openM = document.querySelector('.modal.open, .drawer.open');
  out.modalOpen = !!openM;
  const scope = openM || document.querySelector('.frame') || document.body;
  const desc = (el) => {
    let s = el.tagName.toLowerCase();
    if (el.id) s += '#' + el.id;
    if (el.classList.length) s += '.' + Array.from(el.classList).join('.');
    const txt = (el.innerText || el.getAttribute('aria-label') || el.value || '').trim().replace(/\s+/g, ' ').slice(0, 40);
    return s + (txt ? ` "${txt}"` : '');
  };
  const path = (el) => { const a = []; let e = el; for (let k = 0; e && k < 4 && e !== document.body; k++, e = e.parentElement) a.unshift(e.tagName.toLowerCase() + (e.classList.length ? '.' + Array.from(e.classList).join('.') : '')); return a.join(' > '); };
  const visible = (el) => {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity === 0) return false;
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  };
  const all = Array.from(scope.querySelectorAll('*')).filter(visible);
  // clipped by ancestor?
  const clippedX = (el) => {
    let e = el.parentElement;
    while (e && e !== document.documentElement) {
      const cs = getComputedStyle(e);
      if (cs.overflowX !== 'visible') { const r = e.getBoundingClientRect(); if (r.right <= vw + 1 && r.left >= -1) return e; }
      e = e.parentElement;
    }
    return null;
  };
  // 1. elements beyond viewport
  const beyond = [];
  for (const el of all) {
    if (el.closest('[aria-hidden="true"]') || el.classList.contains('arc')) continue;
    const r = el.getBoundingClientRect();
    if (r.right > vw + 1 || r.left < -1) {
      const c = clippedX(el);
      if (c) continue;
      const par = el.parentElement, pr = par && par.getBoundingClientRect();
      if (pr && (pr.right > vw + 1 || pr.left < -1) && !clippedX(par) && all.includes(par)) continue; // report topmost
      beyond.push({ el: desc(el), path: path(el), left: Math.round(r.left), right: Math.round(r.right), w: Math.round(r.width) });
    }
  }
  out.beyond = beyond.slice(0, 30);
  // 2. inner horizontal scroll containers (intentional or not)
  out.scrollers = all.filter(el => { const cs = getComputedStyle(el); return (cs.overflowX === 'auto' || cs.overflowX === 'scroll') && el.scrollWidth > el.clientWidth + 1; })
    .map(el => ({ el: desc(el).slice(0, 60), sw: el.scrollWidth, cw: el.clientWidth }));
  // 3. text overflow within own box (truncation / spill)
  const spill = [];
  for (const el of all) {
    const cs = getComputedStyle(el);
    if (el.scrollWidth > el.clientWidth + 1 && el.clientWidth > 0 && (cs.overflowX === 'visible' || cs.overflowX === 'hidden' || cs.overflowX === 'clip') && cs.display !== 'inline') {
      const hasText = Array.from(el.childNodes).some(n => n.nodeType === 3 && n.textContent.trim());
      if (!hasText && !el.matches('.btn,.badge,.chip,.tag,.seg>button,.role-tag,.select>button span')) continue;
      if (el.matches('svg,svg *')) continue;
      spill.push({ el: desc(el), path: path(el), sw: el.scrollWidth, cw: el.clientWidth, ov: cs.overflowX, ell: cs.textOverflow === 'ellipsis' });
    }
  }
  out.spill = spill.slice(0, 40);
  // 4. overlaps between leaf text elements
  const leaves = all.filter(el => Array.from(el.childNodes).some(n => n.nodeType === 3 && n.textContent.trim()) && !el.closest('svg') && !el.closest('.heat,.peak,.map,.avatars,.pax'));
  const rects = leaves.map(el => { const range = document.createRange(); range.selectNodeContents(el); const rs = Array.from(range.getClientRects()).filter(x => x.width > 1 && x.height > 1); return rs; });
  const overlaps = [];
  for (let a = 0; a < leaves.length; a++) for (let c = a + 1; c < leaves.length; c++) {
    const A = leaves[a], C = leaves[c];
    if (A.contains(C) || C.contains(A)) continue;
    for (const ra of rects[a]) for (const rc of rects[c]) {
      const ix = Math.min(ra.right, rc.right) - Math.max(ra.left, rc.left), iy = Math.min(ra.bottom, rc.bottom) - Math.max(ra.top, rc.top);
      if (ix > 3 && iy > 3) { overlaps.push({ a: desc(A), b: desc(C), ix: Math.round(ix), iy: Math.round(iy), pa: path(A) }); break; }
    }
    if (overlaps.length > 30) break;
  }
  out.overlaps = overlaps;
  // 5. touch targets
  if (mobile) {
    const sel = 'a[href], button, input:not([type=hidden]), select, textarea, [role=button], .chip, .toggle, [data-open], [data-tab]';
    const small = [];
    for (const el of scope.querySelectorAll(sel)) {
      if (!visible(el)) continue;
      if (el.matches('.input input, .input textarea, .tagbox input')) continue; // wrapper counts
      const r = el.getBoundingClientRect();
      if (r.width < 44 || r.height < 44) small.push({ el: desc(el).slice(0, 70), w: Math.round(r.width), h: Math.round(r.height), path: path(el).slice(-90) });
    }
    out.smallTargets = small;
    // 6. small text
    const tiny = [];
    for (const el of leaves) { const fs = parseFloat(getComputedStyle(el).fontSize); if (fs < 12) tiny.push({ el: desc(el).slice(0, 60), fs, path: path(el).slice(-80) }); }
    out.tinyText = tiny;
    // hide-m visible in modals
    out.hideMVisible = Array.from(document.querySelectorAll('.hide-m')).filter(visible).map(desc);
  }
  // hide-d visible on desktop
  if (!mobile) out.hideDVisible = Array.from(document.querySelectorAll('.hide-d')).filter(visible).map(desc);
  // 7. dialogs
  if (openM) {
    const d = openM.querySelector('.dialog, .panel');
    const r = d.getBoundingClientRect(), cs = getComputedStyle(d);
    out.dialog = { cls: d.className, top: Math.round(r.top), bottom: Math.round(r.bottom), left: Math.round(r.left), right: Math.round(r.right), w: Math.round(r.width), h: Math.round(r.height), sh: d.scrollHeight, ch: d.clientHeight, sw: d.scrollWidth, cw: d.clientWidth, pad: cs.padding, radius: cs.borderRadius };
  }
  // 8. tabbar
  const tb = document.querySelector('.tabbar');
  if (tb && visible(tb)) {
    const r = tb.getBoundingClientRect(), cs = getComputedStyle(tb);
    out.tabbar = { pos: cs.position, top: Math.round(r.top + scrollY), h: Math.round(r.height), docH: document.documentElement.scrollHeight, inViewport: r.top < vh };
  }
  // 9. charts
  out.charts = Array.from(scope.querySelectorAll('.heat-wrap, .bars, .bars-x, .hbar, .peak, .table-wrap, .dist')).filter(visible).map(el => { const r = el.getBoundingClientRect(); return { el: desc(el).slice(0, 40), sw: el.scrollWidth, cw: el.clientWidth, right: Math.round(r.right) }; }).filter(x => x.sw > x.cw + 1 || x.right > vw);
  // bars labels overlap
  const lbls = Array.from(scope.querySelectorAll('.bars .b em, .bars-x span')).filter(visible);
  out.barLabelSpill = lbls.filter(e => e.scrollWidth > e.parentElement.clientWidth + 2).map(e => desc(e) + ' ' + e.scrollWidth + '>' + e.parentElement.clientWidth);
  return out;
}
