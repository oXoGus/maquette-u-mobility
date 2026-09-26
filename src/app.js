/* U-Mobility v3 — interactions de la maquette (pages statiques et aperçu artifact) */
(function () {
  var SPA = !!window.UMOB_SPA;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ---------- Import Figma : ?figma masque la barre de démo et détache la barre d'onglets ---------- */
  if (/[?&]figma\b/.test(location.search)) document.documentElement.classList.add('figma');

  /* ---------- Toasts ---------- */
  function toast(msg) {
    var box = $('.toasts');
    if (!box) { box = document.createElement('div'); box.className = 'toasts'; box.setAttribute('role', 'status'); box.setAttribute('aria-live', 'polite'); document.body.appendChild(box); }
    var t = document.createElement('div');
    t.className = 'toast';
    t.innerHTML = '<svg class="i sm" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12l5 5 9-10"/></svg><span></span>';
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
    // Focus sur le premier champ (ou le bouton principal), pas sur « Fermer »
    var f = $('[data-step]:not([hidden]) input, [data-step]:not([hidden]) textarea', m) || $('input, textarea', m) || $('.dialog-foot .btn:not([data-close]), .btn:not([data-close])', m);
    if (f && f.focus) { try { f.focus({ preventScroll: true }); } catch (e) {} }
    return true;
  }
  function closeModals() { $$('.modal.open, .drawer.open').forEach(function (m) { m.classList.remove('open'); }); }

  /* ---------- Tabs ---------- */
  function activateTab(name) {
    var btn = $('[data-tab="' + name + '"]');
    if (!btn) return false;
    var group = btn.closest('[data-tabs]');
    if (!group) return false;
    var scope = group.getAttribute('data-tabs');
    $$('[data-tab]', group).forEach(function (b) { b.classList.toggle('on', b === btn); });
    $$('[data-panel-of="' + scope + '"]').forEach(function (p) { p.hidden = p.getAttribute('data-panel') !== name; });
    return true;
  }

  /* ---------- Vues d'une même page (ex. trajet.html#membre : passager confirmé) ---------- */
  function applyView(name) {
    var views = $$('[data-view]');
    if (!views.some(function (v) { return v.getAttribute('data-view').split(' ').indexOf(name) >= 0; })) return false;
    views.forEach(function (v) { v.hidden = v.getAttribute('data-view').split(' ').indexOf(name) < 0; });
    // Couleur du mode et titre mobile propres à la vue
    var d = $('[data-view="' + name + '"][data-mode]'), sc = $('.mode-scope');
    if (sc) { var md = (d && d.getAttribute('data-mode')) || sc.getAttribute('data-mode-default'); if (md) sc.className = sc.className.replace(/\bm-[a-z]+\b/g, '').trim() + ' m-' + md; }
    var mt = d && d.getAttribute('data-mtitle'), mb = $('.mobilebar b'); if (mt && mb) mb.textContent = mt;
    // Provenance : bouton retour mobile et entrée active de la navigation
    var w = $('[data-view="' + name + '"][data-back]');
    if (w) {
      var href = w.getAttribute('data-back') + '.html', back = $('.mobilebar a.iconbtn[href]');
      if (back) back.setAttribute('href', href);
      $$('.nav a, .tabbar a').forEach(function (a) {
        var on = a.getAttribute('href') === href;
        a.classList.toggle('active', on);
        if (on) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current');
      });
    }
    return true;
  }

  /* ---------- State from hash (#demande, #conducteur, #loader…) ---------- */
  function applyState(state) {
    if (!state) return;
    if (state === 'loader') { var l = $('#loader'); if (l) l.classList.add('show'); return; }
    if (applyView(state)) return;
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
    if (t && t.classList.contains('tag') && t.querySelector('.tl').offsetWidth > 1) return; // libellé déjà visible
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

  /* ---------- Rôles (maquette) : utilisateur, modérateur, administrateur ---------- */
  var HOME = { user: 'index', mod: 'moderation', admin: 'back-office' };
  function getRole() { try { return sessionStorage.getItem('umob-role') || 'user'; } catch (e) { return window.__umobRole || 'user'; } }
  function setRole(r) { window.__umobRole = r; try { sessionStorage.setItem('umob-role', r); } catch (e) {} }
  function pageRoles() { var app = $('.frame .app') || $('.app'); return app ? (app.getAttribute('data-roles') || '').split(' ').filter(Boolean) : []; }
  function showRole(r) {
    $$('[data-role-view]').forEach(function (v) { v.hidden = v.getAttribute('data-role-view') !== r; });
    $$('.demobar [data-role]').forEach(function (b) { var on = b.getAttribute('data-role') === r; b.classList.toggle('on', on); b.setAttribute('aria-pressed', on); });
  }
  function initRole() {
    var allowed = pageRoles(), r = getRole();
    if (allowed.length && allowed.indexOf(r) < 0) { r = allowed[0]; setRole(r); }
    showRole(r);
  }
  function switchRole(r) {
    setRole(r);
    if (pageRoles().indexOf(r) >= 0) { showRole(r); toast('Vue ' + ({ user: 'utilisateur', mod: 'modérateur', admin: 'administrateur' })[r]); }
    else navigate(HOME[r] + '.html');
  }

  /* ---------- Campus : les zones de départ et points d'arrivée suivent le campus choisi ---------- */
  function setCampus(name) {
    $$('.select').forEach(function (s) {
      var items = $$('[data-campus]', s); if (!items.length) return;
      var first = null;
      items.forEach(function (x) { var on = x.getAttribute('data-campus') === name; x.hidden = !on; if (on && !first && x.classList.contains('opt')) first = x; });
      if (first) { $$('.opt', s).forEach(function (o) { o.classList.toggle('sel', o === first); }); s.querySelector('button > span').textContent = first.textContent; }
    });
    $$('[data-campus-name]').forEach(function (x) { x.textContent = name; });
    toast('Campus ' + name + ' : zones mises à jour');
  }

  /* ---------- Clicks ---------- */
  document.addEventListener('click', function (e) {
    var t = e.target;
    var el;

    if ((el = t.closest('.demobar [data-role]'))) { e.preventDefault(); switchRole(el.getAttribute('data-role')); return; }
    if ((el = t.closest('[data-set-role]'))) setRole(el.getAttribute('data-set-role')); // puis navigation normale du lien
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
    if ((el = t.closest('[data-single] > button'))) {
      $$('button', el.parentNode).forEach(function (b) { b.classList.toggle('on', b === el); if (b.hasAttribute('role')) b.setAttribute('aria-checked', b === el); });
      // data-show="x" ou "groupe:x" : n'affecte que les data-when du même groupe (ex. mode:car / regulier)
      var sw = el.getAttribute('data-show');
      if (sw) {
        var grp = sw.indexOf(':') > 0 ? sw.split(':')[0] + ':' : '';
        // Choix du mode : la zone (formulaire + aperçu) prend la couleur du mode (classe m-car, m-bike…)
        if (grp === 'mode:') { var sc = el.closest('.mode-scope'); if (sc) { sc.className = sc.className.replace(/\bm-[a-z]+\b/g, '').trim() + ' m-' + sw.split(':')[1]; } }
        $$('[data-when]', (grp && el.closest('[data-show-scope]')) || el.closest('.card, .dialog, form, .content') || document).forEach(function (x) {
          var w = x.getAttribute('data-when').split(' ');
          if ((w[0].indexOf(':') > 0 ? w[0].split(':')[0] + ':' : '') !== grp) return;
          x.hidden = w.indexOf(sw) < 0;
        });
        $$('.tagpick', el.closest('[data-show-scope]') || document).forEach(syncTagpick);
      }
      return;
    }
    if ((el = t.closest('.chip[data-toggle]'))) { el.classList.toggle('on'); el.setAttribute('aria-pressed', el.classList.contains('on')); return; }
    if ((el = t.closest('.chip[data-radio]'))) {
      $$('.chip', el.parentNode).forEach(function (b) { b.classList.toggle('on', b === el); });
      // Filtre de liste (Mes trajets) : data-filter = classe que doivent porter les cartes ("" = toutes)
      var fl = el.parentNode.getAttribute('data-filter-list');
      if (fl && el.hasAttribute('data-filter')) { var f = el.getAttribute('data-filter'); $$('#' + fl + ' > .trip').forEach(function (c) { c.hidden = !!f && !c.classList.contains(f); }); }
      return;
    }
    if ((el = t.closest('.toggle'))) { el.classList.toggle('on'); el.setAttribute('aria-pressed', el.classList.contains('on')); return; }
    if ((el = t.closest('.days button'))) { if (!el.classList.contains('off')) el.classList.toggle('on'); return; }
    if ((el = t.closest('.stepper .iconbtn'))) { var b = el.parentNode.querySelector('b'), n = parseInt(b.textContent, 10) + (el.textContent.trim() === '+' ? 1 : -1); var max = parseInt(el.parentNode.getAttribute('data-max') || '8', 10); b.textContent = Math.max(1, Math.min(max, n)); return; }
    if ((el = t.closest('.rate button'))) { setRate(el.parentNode, $$('button', el.parentNode).indexOf(el) + 1); return; }
    if ((el = t.closest('.tagchip'))) { toggleTag(el); return; }
    if ((el = t.closest('.tp-clear'))) { var tp = el.closest('.field').querySelector('.tagpick'); $$('.tagchip.on', tp).forEach(function (b) { setChip(b, false); }); syncTagpick(tp); return; }
    if ((el = t.closest('.select .opt'))) {
      var s = el.closest('.select');
      $$('.opt', s).forEach(function (o) { o.classList.toggle('sel', o === el); });
      s.querySelector('button > span').textContent = el.textContent;
      s.classList.remove('open');
      if (s.hasAttribute('data-campus-ctl')) setCampus(el.textContent);
      return;
    }
    if ((el = t.closest('.select > button'))) { var sel = el.parentNode, was = sel.classList.contains('open'); $$('.select.open').forEach(function (x) { x.classList.remove('open'); }); if (!was) sel.classList.add('open'); return; }
    $$('.select.open').forEach(function (x) { if (!x.contains(t)) x.classList.remove('open'); });
    if ((el = t.closest('.li[data-conv]'))) { $$('.li[data-conv]', el.closest('.list')).forEach(function (x) { x.classList.toggle('sel', x === el); }); return; }
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
  });
  document.addEventListener('input', function (e) {
    var el = e.target;
    if (el.hasAttribute && el.hasAttribute('maxlength')) { var c = el.closest('.field') && el.closest('.field').querySelector('.counter'); if (c) c.textContent = el.value.length + ' / ' + el.getAttribute('maxlength'); }
    if (el.id === 'del-confirm') { var btn = document.getElementById('del-go'); if (btn) { var ok = el.value.trim().toUpperCase() === 'SUPPRIMER'; btn.disabled = !ok; btn.classList.toggle('is-disabled', !ok); } }
  });

  /* ---------- Tags (catalogue fixe) ---------- */
  // Un tap coche, un tap décoche ; data-group : tags qui s'excluent ; data-max sur .tagpick : limite (Publier).
  function setChip(b, on) { b.classList.toggle('on', on); b.setAttribute('aria-pressed', on); }
  function shownOn(box) { return $$('.tagchip.on', box).filter(function (b) { return !b.closest('[hidden]'); }); }
  function toggleTag(el) {
    var box = el.closest('.tagpick'), max = parseInt(box.getAttribute('data-max') || '0', 10);
    var on = !el.classList.contains('on'), g = el.getAttribute('data-group');
    var rivals = g ? $$('.tagchip.on[data-group="' + g + '"]', box).filter(function (b) { return b !== el; }) : [];
    if (on && max && shownOn(box).length - rivals.length >= max) { toast(max + ' tags maximum : retire un tag pour en ajouter un autre'); return; }
    if (on) rivals.forEach(function (b) { setChip(b, false); });
    setChip(el, on); syncTagpick(box);
  }
  function syncTagpick(box) {
    // Un tag masqué (mode changé dans Publier) n'est plus coché
    $$('.tagchip.on', box).forEach(function (b) { if (b.closest('[hidden]')) setChip(b, false); });
    var max = parseInt(box.getAttribute('data-max') || '0', 10), n = shownOn(box).length, f = box.closest('.field');
    $$('.tagchip', box).forEach(function (b) {
      var g = b.getAttribute('data-group'); // un tag qui remplace son rival coché reste disponible
      var dis = !!max && n >= max && !b.classList.contains('on') && !(g && box.querySelector('.tagchip.on[data-group="' + g + '"]'));
      b.classList.toggle('dis', dis); b.setAttribute('aria-disabled', dis);
      if (dis) b.setAttribute('data-tip', max + ' tags maximum'); else b.removeAttribute('data-tip');
    });
    var c = f && f.querySelector('.tp-count b'); if (c) c.textContent = n;
    var x = f && f.querySelector('.tp-clear'); if (x) x.hidden = !n;
  }

  /* ---------- SPA router (artifact) ---------- */
  function navigate(href, noLoader) {
    var parts = href.split('#'), page = parts[0].replace('.html', ''), state = parts[1] || '';
    if (!window.UMOB_render) { loader(350, function () { location.href = href; }); return; } // pages statiques
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
    initRole();
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
