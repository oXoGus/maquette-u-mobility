/* U-Mobility v2 — interactions de la maquette (pages statiques et aperçu artifact) */
(function () {
  var SPA = !!window.UMOB_SPA;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ---------- Toasts ---------- */
  function toast(msg) {
    var box = $('.toasts');
    if (!box) { box = document.createElement('div'); box.className = 'toasts'; document.body.appendChild(box); }
    var t = document.createElement('div');
    t.className = 'toast';
    t.innerHTML = '<svg class="i sm" viewBox="0 0 24 24"><path d="M5 12l5 5 9-10"/></svg><span></span>';
    t.querySelector('span').textContent = msg;
    box.appendChild(t);
    setTimeout(function () { t.remove(); }, 2600);
  }

  /* ---------- Loader ---------- */
  function loader(ms, cb) {
    var l = $('#loader');
    if (!l) { if (cb) cb(); return; }
    l.classList.add('show');
    setTimeout(function () { l.classList.remove('show'); if (cb) cb(); }, ms || 600);
  }

  /* ---------- Loader : tirets de la route en perspective (mêmes constantes que le logo) ---------- */
  var VPY = 495.3, K = 0.196, R = 1.94, Q = 1.63, D0 = 84;
  function roadPolys(s) {
    var out = '';
    for (var n = -2; n < 5; n++) {
      var d1 = D0 * Math.pow(R, n + s), d2 = d1 * Q, y1 = VPY + d1, y2 = VPY + d2;
      if (y1 > 1160) continue;
      var c1 = 457.3 + 0.0088 * (y1 - 582), c2 = 457.3 + 0.0088 * (y2 - 582);
      out += '<polygon points="' + (c1 - K * d1).toFixed(1) + ',' + y1.toFixed(1) + ' ' + (c1 + K * d1).toFixed(1) + ',' + y1.toFixed(1) + ' ' + (c2 + K * d2).toFixed(1) + ',' + y2.toFixed(1) + ' ' + (c2 - K * d2).toFixed(1) + ',' + y2.toFixed(1) + '"/>';
    }
    return out;
  }
  var t0 = 0, still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function tick(t) {
    if (!t0) t0 = t;
    var s = ((t - t0) / 900) % 1;
    $$('.loader.show [data-road], .loader-inline [data-road]').forEach(function (g) { g.innerHTML = roadPolys(s); });
    requestAnimationFrame(tick);
  }
  if (!still && window.requestAnimationFrame) requestAnimationFrame(tick);

  /* ---------- Modals & drawers ---------- */
  function openModal(id) {
    var m = document.getElementById('m-' + id);
    if (!m) return false;
    $$('.modal.open, .drawer.open').forEach(function (x) { if (x !== m) x.classList.remove('open'); });
    var steps = $$('[data-step]', m);
    if (steps.length) steps.forEach(function (s, k) { s.hidden = k !== 0; });
    m.classList.add('open');
    var f = $('input, textarea, button', m); if (f && f.focus) { try { f.focus({ preventScroll: true }); } catch (e) {} }
    return true;
  }
  function closeModals() { $$('.modal.open, .drawer.open').forEach(function (m) { m.classList.remove('open'); }); }

  /* ---------- Tabs ---------- */
  function activateTab(name) {
    var btn = $('[data-tab="' + name + '"]');
    if (!btn) return false;
    var group = btn.closest('[data-tabs]');
    var scope = group.getAttribute('data-tabs');
    $$('[data-tab]', group).forEach(function (b) { b.classList.toggle('on', b === btn); });
    $$('[data-panel-of="' + scope + '"]').forEach(function (p) { p.hidden = p.getAttribute('data-panel') !== name; });
    return true;
  }

  /* ---------- State from hash (#demande, #conducteur, #loader…) ---------- */
  function applyState(state) {
    if (!state) return;
    if (state === 'loader') { var l = $('#loader'); if (l) l.classList.add('show'); return; }
    if (activateTab(state)) return;
    openModal(state);
  }

  /* ---------- Heatmap tooltip ---------- */
  var tip;
  function showTip(e, text) {
    if (!tip) { tip = document.createElement('div'); tip.className = 'tip'; document.body.appendChild(tip); }
    tip.textContent = text; tip.hidden = false;
    var r = e.target.getBoundingClientRect();
    tip.style.left = (r.left + r.width / 2) + 'px'; tip.style.top = r.top + 'px';
  }
  document.addEventListener('mouseover', function (e) {
    var t = e.target.closest && e.target.closest('[data-tip]');
    if (t) showTip({ target: t }, t.getAttribute('data-tip'));
  });
  document.addEventListener('mouseout', function (e) {
    if (tip && e.target.closest && e.target.closest('[data-tip]')) tip.hidden = true;
  });

  /* ---------- Star rating ---------- */
  var LABELS = ['', 'Très décevant', 'Décevant', 'Correct', 'Bien', 'Excellent'];
  function setRate(r, v) {
    r.setAttribute('data-value', v);
    $$('button', r).forEach(function (b, k) { b.classList.toggle('on', k < v); });
    var lbl = r.parentNode.querySelector('.rate-label'); if (lbl) lbl.textContent = v ? LABELS[v] : 'Choisis une note';
  }
  document.addEventListener('mouseover', function (e) {
    var b = e.target.closest && e.target.closest('.rate button');
    if (!b) return;
    var r = b.parentNode, k = $$('button', r).indexOf(b);
    r.classList.add('hovering');
    $$('button', r).forEach(function (x, j) { x.classList.toggle('hov', j <= k); });
  });
  document.addEventListener('mouseout', function (e) {
    var r = e.target.closest && e.target.closest('.rate');
    if (r && !r.contains(e.relatedTarget)) r.classList.remove('hovering');
  });

  /* ---------- Clicks ---------- */
  document.addEventListener('click', function (e) {
    var t = e.target;
    var el;

    if ((el = t.closest('[data-open]'))) { e.preventDefault(); e.stopPropagation(); openModal(el.getAttribute('data-open')); return; }
    if ((el = t.closest('[data-close]'))) { e.preventDefault(); closeModals(); if (el.hasAttribute('data-toast')) toast(el.getAttribute('data-toast')); return; }
    if (t.classList && (t.classList.contains('modal') || t.classList.contains('drawer'))) { closeModals(); return; }
    if ((el = t.closest('[data-next]'))) {
      e.preventDefault();
      var dlg = el.closest('.modal, .drawer');
      var go = function () {
        var steps = $$('[data-step]', dlg), cur = steps.filter(function (s) { return !s.hidden; })[0], k = steps.indexOf(cur);
        if (steps[k + 1]) { cur.hidden = true; steps[k + 1].hidden = false; }
      };
      if (el.hasAttribute('data-loading')) {
        var html = el.innerHTML; el.innerHTML = '<span class="spin"></span>Envoi…'; el.disabled = true;
        setTimeout(function () { el.innerHTML = html; el.disabled = false; go(); }, 900);
      } else go();
      return;
    }
    if ((el = t.closest('[data-loadtoast]'))) { e.preventDefault(); var msg = el.getAttribute('data-loadtoast'); loader(800, function () { toast(msg); }); return; }
    if ((el = t.closest('[data-tab]'))) { e.preventDefault(); activateTab(el.getAttribute('data-tab')); return; }
    if ((el = t.closest('[data-toast]'))) { e.preventDefault(); toast(el.getAttribute('data-toast')); if (el.hasAttribute('data-remove')) { var c = el.closest(el.getAttribute('data-remove')); if (c) { c.style.transition = 'opacity .2s'; c.style.opacity = '0'; setTimeout(function () { c.remove(); }, 200); } } return; }
    if ((el = t.closest('.seg[data-single] > button'))) { $$('button', el.parentNode).forEach(function (b) { b.classList.toggle('on', b === el); }); var sw = el.getAttribute('data-show'); if (sw) { $$('[data-when]', el.closest('.card, .dialog, form, .content') || document).forEach(function (x) { x.hidden = x.getAttribute('data-when') !== sw; }); } return; }
    if ((el = t.closest('.chip[data-toggle]'))) { el.classList.toggle('on'); return; }
    if ((el = t.closest('.chip[data-radio]'))) { $$('.chip', el.parentNode).forEach(function (b) { b.classList.toggle('on', b === el); }); return; }
    if ((el = t.closest('.toggle'))) { el.classList.toggle('on'); el.setAttribute('aria-pressed', el.classList.contains('on')); return; }
    if ((el = t.closest('.days button'))) { if (!el.classList.contains('off')) el.classList.toggle('on'); return; }
    if ((el = t.closest('.stepper .iconbtn'))) { var b = el.parentNode.querySelector('b'), n = parseInt(b.textContent, 10) + (el.textContent.trim() === '+' ? 1 : -1); var max = parseInt(el.parentNode.getAttribute('data-max') || '8', 10); b.textContent = Math.max(1, Math.min(max, n)); return; }
    if ((el = t.closest('.rate button'))) { setRate(el.parentNode, $$('button', el.parentNode).indexOf(el) + 1); return; }
    if ((el = t.closest('.tag button'))) { el.parentNode.remove(); return; }
    if ((el = t.closest('.suggest button'))) { addTag(el.closest('.field').querySelector('.tagbox'), el.textContent.replace(/^\+\s*/, '')); el.remove(); return; }
    if ((el = t.closest('.select .opt'))) {
      var s = el.closest('.select');
      $$('.opt', s).forEach(function (o) { o.classList.toggle('sel', o === el); });
      s.querySelector('button > span').textContent = el.textContent;
      s.classList.remove('open'); return;
    }
    if ((el = t.closest('.select > button'))) { var sel = el.parentNode, was = sel.classList.contains('open'); $$('.select.open').forEach(function (x) { x.classList.remove('open'); }); if (!was) sel.classList.add('open'); return; }
    $$('.select.open').forEach(function (x) { if (!x.contains(t)) x.classList.remove('open'); });
    if ((el = t.closest('.li[data-conv]'))) { $$('.li[data-conv]').forEach(function (x) { x.classList.toggle('sel', x === el); }); return; }
    if ((el = t.closest('[data-logout]'))) { e.preventDefault(); navigate('connexion.html'); return; }

    // Navigation
    var a = t.closest('a[href]');
    if (a && SPA) {
      var href = a.getAttribute('href');
      if (/^[a-z0-9-]+\.html(#[a-z0-9-]+)?$/i.test(href)) { e.preventDefault(); navigate(href); }
    } else if (a && /\.html(#.*)?$/.test(a.getAttribute('href') || '')) {
      // pages statiques : petit loader avant de changer de page
      var h = a.getAttribute('href');
      if (!e.metaKey && !e.ctrlKey && $('#loader')) { e.preventDefault(); loader(350, function () { location.href = h; }); }
    }
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { closeModals(); $$('.select.open').forEach(function (x) { x.classList.remove('open'); }); }
    var inp = e.target;
    if (e.key === 'Enter' && inp.matches && inp.matches('.tagbox input')) { e.preventDefault(); addTag(inp.closest('.tagbox'), inp.value); inp.value = ''; }
  });
  document.addEventListener('input', function (e) {
    var el = e.target;
    if (el.hasAttribute && el.hasAttribute('maxlength')) { var c = el.closest('.field') && el.closest('.field').querySelector('.counter'); if (c) c.textContent = el.value.length + ' / ' + el.getAttribute('maxlength'); }
    if (el.id === 'del-confirm') { var btn = document.getElementById('del-go'); if (btn) { var ok = el.value.trim().toUpperCase() === 'SUPPRIMER'; btn.disabled = !ok; btn.classList.toggle('is-disabled', !ok); } }
  });

  // Même calcul que hue()/tagc() dans build.py : un tag garde sa couleur partout.
  function tagColor(text) {
    var n = 0, s = text.toLowerCase();
    for (var k = 0; k < s.length; k++) n = (n * 123 + s.charCodeAt(k)) % 1000003;
    return 't' + (n % 6);
  }

  function addTag(box, text) {
    text = (text || '').trim().replace(/^#/, '');
    if (!box || !text) return;
    var t = document.createElement('span'); t.className = 'tag ' + tagColor(text);
    t.innerHTML = '<span></span><button type="button" aria-label="Retirer"><svg class="i sm" viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></svg></button>';
    t.firstChild.textContent = text;
    box.insertBefore(t, box.querySelector('input'));
  }

  /* ---------- SPA router (artifact) ---------- */
  function navigate(href, noLoader) {
    var parts = href.split('#'), page = parts[0].replace('.html', ''), state = parts[1] || '';
    if (!window.UMOB_render) return;
    var go = function () {
      window.UMOB_render(page);
      var h = '#' + page + (state ? '.' + state : '');
      if (location.hash !== h) { try { history.replaceState(null, '', h); } catch (e) { location.hash = h; } }
      window.scrollTo(0, 0);
      init(); applyState(state);
    };
    if (noLoader) go(); else loader(450, go);
  }
  window.UMOB_navigate = navigate;

  function init() {
    $$('.rate').forEach(function (r) { setRate(r, parseInt(r.getAttribute('data-value') || '0', 10)); });
  }

  if (SPA) {
    window.addEventListener('DOMContentLoaded', function () {
      var h = (location.hash || '').slice(1), p = h.split('.');
      navigate((p[0] || 'plan') + '.html' + (p[1] ? '#' + p[1] : ''), true);
    });
  } else {
    window.addEventListener('DOMContentLoaded', function () { init(); applyState((location.hash || '').slice(1)); });
    window.addEventListener('hashchange', function () { closeModals(); applyState((location.hash || '').slice(1)); });
  }
})();
