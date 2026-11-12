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
    $$('[data-guard]', m).forEach(guard);
    // Focus sur le premier champ (ou le bouton principal), pas sur « Fermer »
    var f = $('[data-step]:not([hidden]) input, [data-step]:not([hidden]) textarea', m) || $('input, textarea', m) || $('.dialog-foot .btn:not([data-close]), .btn:not([data-close])', m);
    if (f && f.focus) { try { f.focus({ preventScroll: true }); } catch (e) {} }
    return true;
  }
  function closeModals() { $$('.modal.open, .drawer.open').forEach(function (m) { m.classList.remove('open'); }); }

  /* ---------- Envoi bloqué tant que le formulaire est incomplet (signalements) ---------- */
  // [data-guard] : étape ; [data-req] : case à cocher obligatoire, ou champ de data-req caractères au moins ; [data-guarded] : bouton d'envoi.
  function guard(step) {
    var ok = $$('[data-req]', step).every(function (x) {
      if (x.type === 'checkbox') return x.checked;
      return x.value.trim().length >= parseInt(x.getAttribute('data-req') || '1', 10);
    });
    $$('[data-guarded]', step).forEach(function (b) { b.disabled = !ok; });
  }

  /* ---------- Mini-profil d'une personne (#m-profil), rempli avec le data-person cliqué ---------- */
  // data-person : nom|initiales|couleur|formation|note|trajets|réponse|mention|ensemble (person_data() dans build.py)
  function setAvatar(av, d) { av.textContent = d[1]; av.className = av.className.replace(/\bav\d\b/, '').trim() + ' ' + d[2]; }
  function fillPerson(el) {
    var data = el.getAttribute('data-person'), d = data.split('|'), m = document.getElementById('m-profil');
    if (!m) return;
    var f = function (k) { return $('[data-p="' + k + '"]', m); };
    f('name').textContent = d[0]; f('sub').textContent = d[3]; f('rate').textContent = d[4]; f('trips').textContent = d[5];
    setAvatar(f('ini'), d);
    [['reply', d[6] ? 'Répond en moyenne en ' + d[6] : ''], ['note', d[7]], ['together', d[8]]].forEach(function (x) {
      var b = f(x[0]); if (!b) return; b.hidden = !x[1]; b.querySelector('span').textContent = x[1];
    });
    // « Signaler ce compte » visera cette personne
    var rep = $('[data-open="signaler-compte"]', m);
    if (rep) { rep.setAttribute('data-person', data); rep.setAttribute('aria-label', 'Signaler le compte de ' + d[0]); }
  }

  /* ---------- Signaler un compte : depuis une personne (data-person), elle est déjà choisie et la liste disparaît ---------- */
  function reportTarget(data) {
    var m = document.getElementById('m-signaler-compte');
    if (!m) return;
    var tg = $('.report-target', m), pick = $('.report-pick', m);
    tg.hidden = !data; pick.hidden = !!data;
    if (!data) return;
    var d = data.split('|');
    setAvatar($('[data-r="ini"]', tg), d);
    $('[data-r="name"]', tg).textContent = d[0]; $('[data-r="sub"]', tg).textContent = d[3];
  }

  /* ---------- Images d'un signalement : 5 au plus, ajout et retrait ---------- */
  var upUid = 2;
  function uploadAction(el) {
    var box = el.closest('.up-field'), list = $('.uploads', box), max = parseInt(box.getAttribute('data-max') || '5', 10);
    if (el.getAttribute('data-upload') === 'add') {
      var n = $$('.up', list).length; if (n >= max) return;
      var li = $('.up-tpl', box).content.firstElementChild.cloneNode(true), name = 'capture-' + (++upUid) + '.jpg';
      li.className = 'up t' + (n % 3 + 1);
      $('.up-name', li).textContent = name; $('.up-img', li).setAttribute('aria-label', 'Image ' + name);
      $('.up-del', li).setAttribute('aria-label', 'Retirer ' + name);
      list.insertBefore(li, $('.up-add-li', list)); toast('Image ajoutée');
    } else { el.closest('.up').remove(); toast('Image retirée'); }
    var k = $$('.up', list).length, add = $('.up-add', box), full = k >= max;
    $('.tp-count b', box).textContent = k;
    add.disabled = full; $('span', add).textContent = full ? max + ' images maximum' : 'Ajouter';
    if (!full) add.focus();
  }

  /* ---------- Groupes data-show / data-when ---------- */
  // data-show="x" ou "groupe:x" : n'affecte que les data-when du même groupe (ex. mode:car / regulier / sens:aller)
  function applyShow(scope, grp, sw) {
    $$('[data-when]', scope).forEach(function (x) {
      var w = x.getAttribute('data-when').split(' ');
      if ((w[0].indexOf(':') > 0 ? w[0].split(':')[0] + ':' : '') !== grp) return;
      x.hidden = w.indexOf(sw) < 0;
    });
  }
  function setModeClass(el, mode) { el.className = el.className.replace(/\bm-[a-z]+\b/g, '').trim() + ' m-' + mode; }

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

  /* ---------- Messagerie : en mobile, la liste seule puis la conversation seule ---------- */
  // .in-conv sur .app (styles.css) ; le titre du trajet passe dans la barre mobile, le bouton retour revient à la liste.
  function isMobileLayout() { var l = $('.conv-list'); return !!l && getComputedStyle(l).display === 'none'; }
  function openConv(li) {
    var app = $('.app'), mb = $('.mobilebar b'), back = $('.mobilebar a.iconbtn[href]');
    if (!app || !li) return;
    $$('.li[data-conv]').forEach(function (x) { var on = x === li; x.classList.toggle('sel', on); if (on) x.setAttribute('aria-current', 'true'); else x.removeAttribute('aria-current'); });
    app.classList.add('in-conv');
    if (mb) { if (!mb.hasAttribute('data-title')) mb.setAttribute('data-title', mb.textContent); mb.textContent = li.getAttribute('data-conv-title'); }
    if (back) { back.setAttribute('data-conv-back', ''); back.setAttribute('aria-label', 'Retour aux conversations'); }
    // Mobile : on arrive sur les derniers messages, juste au-dessus de la saisie
    if (isMobileLayout()) window.scrollTo(0, document.documentElement.scrollHeight);
  }
  function closeConv() {
    var app = $('.app'), mb = $('.mobilebar b'), back = $('.mobilebar a.iconbtn[data-conv-back]');
    if (!app) return;
    app.classList.remove('in-conv');
    if (mb && mb.hasAttribute('data-title')) mb.textContent = mb.getAttribute('data-title');
    if (back) { back.removeAttribute('data-conv-back'); back.setAttribute('aria-label', 'Retour'); }
    window.scrollTo(0, 0);
    var sel = $('.li[data-conv].sel'); if (sel) { try { sel.focus({ preventScroll: true }); } catch (e) {} }
  }

  /* ---------- Blocs repliables (mobile) : filtres et formulaire de la recherche, sections du Profil ---------- */
  // data-collapse="libellé fermé|libellé ouvert" : aria-label du bouton s'il en a un, sinon le texte de son <span>.
  function setCollapse(cb, open) {
    cb.classList.toggle('open', open);
    $$('[data-collapse]', cb).filter(function (b) { return b.closest('.collapsible') === cb; }).forEach(function (b) {
      b.setAttribute('aria-expanded', open);
      var lb = (b.getAttribute('data-collapse') || '').split('|');
      if (lb.length !== 2) return;
      if (b.hasAttribute('aria-label')) b.setAttribute('aria-label', open ? lb[1] : lb[0]);
      else { var sp = b.querySelector('span'); if (sp) sp.textContent = open ? lb[1] : lb[0]; }
    });
  }

  /* ---------- Pagination (maquette : seule la page active change) ---------- */
  function setPage(el) {
    var pg = el.closest('.pager'), max = parseInt(pg.getAttribute('data-pages'), 10), cur = $('.pg-n.on', pg);
    var n = el.getAttribute('data-page'), c = parseInt(cur.getAttribute('data-page'), 10);
    n = n === 'prev' ? c - 1 : n === 'next' ? c + 1 : parseInt(n, 10);
    if (n < 1 || n > max) return;
    $$('.pg-n', pg).forEach(function (b) {
      var on = parseInt(b.getAttribute('data-page'), 10) === n;
      b.classList.toggle('on', on);
      if (on) b.setAttribute('aria-current', 'page'); else b.removeAttribute('aria-current');
    });
    $('[data-page="prev"]', pg).disabled = n === 1;
    $('[data-page="next"]', pg).disabled = n === max;
    var out = $('[data-page-cur]'); if (out) out.textContent = n;
    var list = pg.closest('.stack'); if (list) list.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  /* ---------- State from hash (#demande, #conducteur, #loader…) ---------- */
  function applyState(state) {
    if (!state) return;
    // Messagerie : chaque état (popup comprise) se joue dans la conversation ouverte
    if ($('.chat-layout')) { openConv($('.li[data-conv].sel') || $('.li[data-conv]')); if (state === 'conversation') return; }
    // Bloc repliable ouvert par son ancre (recherche.html#filtres, #modifier)
    var cs = $$('.collapsible[data-state~="' + state + '"]'); if (cs.length) { cs.forEach(function (c) { setCollapse(c, true); }); return; }
    if (state === 'loader') { var l = $('#loader'); if (l) l.classList.add('show'); return; }
    if (state === 'signaler-profil') { var rb = $('#m-profil [data-open="signaler-compte"]'); reportTarget(rb && rb.getAttribute('data-person')); openModal('signaler-compte'); return; }
    if (applyView(state)) return;
    if (activateTab(state)) return;
    // Popup propre à une vue (ex. #demande-pied sur la vue #pied) : la vue d'abord
    var iv = $('#m-' + state + ' [data-in-view]'); if (iv) applyView(iv.getAttribute('data-in-view'));
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

    if ((el = t.closest('[data-conv-back]'))) { e.preventDefault(); closeConv(); return; }
    if ((el = t.closest('.demobar [data-role]'))) { e.preventDefault(); switchRole(el.getAttribute('data-role')); return; }
    if ((el = t.closest('[data-set-role]'))) setRole(el.getAttribute('data-set-role')); // puis navigation normale du lien
    if ((el = t.closest('[data-open]'))) {
      e.preventDefault(); e.stopPropagation();
      var oid = el.getAttribute('data-open');
      if (oid === 'profil' && el.hasAttribute('data-person')) fillPerson(el);
      if (oid === 'signaler-compte') reportTarget(el.getAttribute('data-person'));
      openModal(oid); return;
    }
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
    if ((el = t.closest('[data-loadtoast]'))) {
      e.preventDefault(); var msg = el.getAttribute('data-loadtoast'), fold = el.closest('.collapsible.open');
      // Recherche (mobile) : le formulaire se replie pour laisser voir les résultats
      loader(800, function () { if (fold) setCollapse(fold, false); toast(msg); }); return;
    }
    if ((el = t.closest('[data-tab]'))) { e.preventDefault(); activateTab(el.getAttribute('data-tab')); return; }
    if ((el = t.closest('[data-toast]'))) { e.preventDefault(); toast(el.getAttribute('data-toast')); if (el.hasAttribute('data-remove')) { var c = el.closest(el.getAttribute('data-remove')); if (c) { c.style.transition = 'opacity .2s'; c.style.opacity = '0'; setTimeout(function () { c.remove(); }, 200); } } return; }
    if ((el = t.closest('[data-scroll]'))) { var tg = document.getElementById(el.getAttribute('data-scroll')); if (tg) { tg.scrollIntoView({ behavior: still ? 'auto' : 'smooth', block: 'start' }); tg.setAttribute('tabindex', '-1'); tg.focus({ preventScroll: true }); } return; }
    if ((el = t.closest('[data-stop]'))) { e.preventDefault(); stopAction(el); return; }
    if ((el = t.closest('[data-upload]'))) { e.preventDefault(); uploadAction(el); return; }
    if ((el = t.closest('[data-single] > button'))) {
      // Demande de réservation : le point de montée choisi s'affiche dans le récapitulatif
      if (el.hasAttribute('data-label')) { var bo = el.closest('.dialog, .modal') && el.closest('.dialog, .modal').querySelector('[data-board-out]'); if (bo) bo.textContent = el.getAttribute('data-label'); }
      $$('button', el.parentNode).forEach(function (b) { b.classList.toggle('on', b === el); if (b.hasAttribute('role')) b.setAttribute('aria-checked', b === el); });
      var sw = el.getAttribute('data-show');
      if (sw) {
        var grp = sw.indexOf(':') > 0 ? sw.split(':')[0] + ':' : '';
        // Choix du mode : la zone (formulaire + aperçu) prend la couleur du mode (classe m-car, m-bike…)
        if (grp === 'mode:') { var sc = el.closest('.mode-scope'); if (sc) setModeClass(sc, sw.split(':')[1]); }
        applyShow((grp && el.closest('[data-show-scope]')) || el.closest('.card, .dialog, form, .content') || document, grp, sw);
        // Publier : la popup de confirmation (hors du formulaire) recopie les choix et la couleur du mode
        if (el.closest('[data-show-scope]')) $$('[data-show-mirror]').forEach(function (mr) { if (grp === 'mode:') setModeClass(mr, sw.split(':')[1]); applyShow(mr, grp, sw); });
        $$('.tagpick', el.closest('[data-show-scope]') || document).forEach(syncTagpick);
      }
      return;
    }
    if ((el = t.closest('.chip[data-toggle]'))) { el.classList.toggle('on'); el.setAttribute('aria-pressed', el.classList.contains('on')); return; }
    if ((el = t.closest('.chip[data-radio]'))) {
      $$('.chip', el.parentNode).forEach(function (b) { b.classList.toggle('on', b === el); });
      // Filtre de liste (Mes trajets) : data-filter = classe que doivent porter les cartes ("" = toutes) ;
      // une section [data-filter-sec] sans carte visible est masquée
      var fl = el.parentNode.getAttribute('data-filter-list');
      if (fl && el.hasAttribute('data-filter')) {
        var f = el.getAttribute('data-filter');
        $$('#' + fl + ' .trip').forEach(function (c) { c.hidden = !!f && !c.classList.contains(f); });
        $$('#' + fl + ' [data-filter-sec]').forEach(function (sec) { sec.hidden = !$$('.trip', sec).some(function (c) { return !c.hidden; }); });
      }
      return;
    }
    if ((el = t.closest('[data-collapse]'))) { var cb = el.closest('.collapsible'); setCollapse(cb, !cb.classList.contains('open')); return; }
    if ((el = t.closest('.pager [data-page]'))) { setPage(el); return; }
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
    if ((el = t.closest('.li[data-conv]'))) { openConv(el); return; }
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
    if (el.hasAttribute && el.hasAttribute('maxlength')) {
      var c = el.closest('.field') && el.closest('.field').querySelector('.counter'), min = parseInt(el.getAttribute('data-req') || '0', 10), len = el.value.trim().length;
      if (c) c.textContent = len < min ? 'Encore ' + (min - len) + ' caractère' + (min - len > 1 ? 's' : '') : el.value.length + ' / ' + el.getAttribute('maxlength');
    }
    var gd = el.closest && el.closest('[data-guard]'); if (gd) guard(gd);
    // Publier : la description saisie est recopiée dans le récapitulatif (popup #confirmer), masqué si elle est vide
    if (el.id === 'p-desc') $$('[data-desc-out]').forEach(function (o) { o.textContent = el.value.trim(); var b = o.closest('.trip-desc'); if (b) b.hidden = !el.value.trim(); });
    var sf = el.closest && (el.closest('.stops-field') || ((el.id === 'p-dep-t' || el.id === 'p-arr-t') && $('.stops-field')));
    if (sf) syncStops(sf);
    if (el.id === 'del-confirm') { var btn = document.getElementById('del-go'); if (btn) { var ok = el.value.trim().toUpperCase() === 'SUPPRIMER'; btn.disabled = !ok; btn.classList.toggle('is-disabled', !ok); } }
  });
  document.addEventListener('change', function (e) { var gd = e.target.closest && e.target.closest('[data-guard]'); if (gd) guard(gd); });

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

  /* ---------- Étapes (Publier) : 2 au plus, zone + heure estimée, ordonnées à la main ---------- */
  var stopUid = 0;
  function toMin(v) { var m = (v || '').match(/(\d{1,2})\s*h\s*(\d{0,2})/); return m ? +m[1] * 60 + (+m[2] || 0) : null; }
  var STOP_LBL = { up: "Avancer l'étape ", down: "Reculer l'étape ", del: "Retirer l'étape " };
  function syncStops(box) {
    var rows = $$('.stops > .stop-row', box), max = parseInt(box.getAttribute('data-max') || '2', 10);
    rows.forEach(function (r, k) {
      var n = k + 1;
      r.querySelector('.stop-n').textContent = n;
      r.querySelector('.field .label').textContent = "Zone de l'étape " + n;
      $$('[data-stop]', r).forEach(function (b) { b.setAttribute('aria-label', STOP_LBL[b.getAttribute('data-stop')] + n); });
      r.querySelector('[data-stop="up"]').disabled = k === 0;
      r.querySelector('[data-stop="down"]').disabled = k === rows.length - 1;
    });
    var add = $('.stop-add', box), full = rows.length >= max;
    if (add) { add.disabled = full; add.lastChild.textContent = full ? max + ' étapes maximum' : 'Ajouter une étape'; }
    var c = $('.tp-count b', box); if (c) c.textContent = rows.length;
    // Les heures suivent l'ordre du parcours : départ < étape 1 < étape 2 < arrivée
    var dep = $('#p-dep-t'), arr = $('#p-arr-t'), prev = dep ? toMin(dep.value) : null, end = arr ? toMin(arr.value) : null, bad = false;
    rows.forEach(function (r) {
      var v = toMin(r.querySelector('input').value);
      var ko = v !== null && ((prev !== null && v <= prev) || (end !== null && v >= end));
      r.classList.toggle('bad', ko); bad = bad || ko;
      if (v !== null) prev = v;
    });
    var w = $('.stop-warn', box); if (w) w.hidden = !bad;
  }
  function stopAction(el) {
    var box = el.closest('.stops-field'), list = $('.stops', box), act = el.getAttribute('data-stop'), row = el.closest('.stop-row');
    if (act === 'add') {
      if ($$('.stop-row', list).length >= parseInt(box.getAttribute('data-max') || '2', 10)) return;
      var tpl = $('.stop-tpl', box), li = tpl.content.firstElementChild.cloneNode(true);
      stopUid++;
      $$('[id]', li).forEach(function (x) { x.id = x.id.replace('p-stop0', 'p-stop-n' + stopUid); });
      $$('label[for]', li).forEach(function (x) { x.setAttribute('for', x.getAttribute('for').replace('p-stop0', 'p-stop-n' + stopUid)); });
      list.appendChild(li); syncStops(box);
      li.querySelector('.select > button').focus();
    } else if (act === 'del') {
      row.remove(); syncStops(box); toast('Étape retirée');
      var b = $('.stop-add', box); if (b) b.focus();
    } else if (act === 'up' && row.previousElementSibling) {
      list.insertBefore(row, row.previousElementSibling); syncStops(box); (el.disabled ? row.querySelector('[data-stop="down"]') : el).focus();
    } else if (act === 'down' && row.nextElementSibling) {
      list.insertBefore(row.nextElementSibling, row); syncStops(box); (el.disabled ? row.querySelector('[data-stop="up"]') : el).focus();
    }
  }

  /* ---------- Statistiques : les nombres montent de 0 à leur valeur (courbe de Bézier cubique) ---------- */
  // Même syntaxe que cubic-bezier() en CSS : x(t) est résolu par Newton puis dichotomie, on renvoie y(t).
  function cubicBezier(x1, y1, x2, y2) {
    var cx = 3 * x1, bx = 3 * (x2 - x1) - cx, ax = 1 - cx - bx;
    var cy = 3 * y1, by = 3 * (y2 - y1) - cy, ay = 1 - cy - by;
    function sx(t) { return ((ax * t + bx) * t + cx) * t; }
    function sy(t) { return ((ay * t + by) * t + cy) * t; }
    function dx(t) { return (3 * ax * t + 2 * bx) * t + cx; }
    return function (x) {
      if (x <= 0) return 0; if (x >= 1) return 1;
      var t = x, i, d;
      for (i = 0; i < 8; i++) { var e = sx(t) - x; if (Math.abs(e) < 1e-6) return sy(t); d = dx(t); if (Math.abs(d) < 1e-6) break; t -= e / d; }
      var lo = 0, hi = 1; t = x;
      while (hi - lo > 1e-6) { if (sx(t) < x) lo = t; else hi = t; t = (lo + hi) / 2; }
      return sy(t);
    };
  }
  var COUNT_EASE = cubicBezier(0.22, 1, 0.36, 1), COUNT_MS = 1200;
  function fmtFr(n, dec) { // format français : espace fine insécable pour les milliers, virgule décimale
    var p = n.toFixed(dec).split('.');
    return p[0].replace(/\B(?=(\d{3})+(?!\d))/g, ' ') + (p[1] ? ',' + p[1] : '');
  }
  function countUp(el) { // affiche 0 et renvoie la fonction qui lance la montée
    var node = el.firstChild;
    if (!node || node.nodeType !== 3) return;
    var m = node.nodeValue.match(/^(\s*)([\d\s  ]*\d(?:,\d+)?)(.*)$/);
    if (!m) return;
    var to = parseFloat(m[2].replace(/[\s  ]/g, '').replace(',', '.')), dec = (m[2].split(',')[1] || '').length;
    var sep = /[\s  ]/.test(m[2]) ? m[2].match(/[\s  ]/)[0] : ' ';
    var fmt = function (v) { return m[1] + fmtFr(v, dec).replace(/ /g, sep) + m[3]; };
    node.nodeValue = fmt(0);
    return function () {
      var t0 = null;
      requestAnimationFrame(function step(now) {
        if (t0 === null) t0 = now;
        var k = Math.min(1, (now - t0) / COUNT_MS);
        node.nodeValue = k < 1 ? fmt(to * COUNT_EASE(k)) : m[1] + m[2] + m[3]; // valeur finale : texte d'origine
        if (k < 1) requestAnimationFrame(step);
      });
    };
  }
  function initCounters() {
    var els = $$('.stat .v').filter(function (el) { return !el.hasAttribute('data-counted'); });
    els.forEach(function (el) { el.setAttribute('data-counted', ''); });
    // Pas d'animation pour l'import Figma (valeurs finales) ni si l'utilisateur réduit les animations
    if (document.documentElement.classList.contains('figma') || (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches)) return;
    var io = 'IntersectionObserver' in window && new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { io.unobserve(e.target); e.target._count(); } });
    }, { threshold: 0.4 });
    els.forEach(function (el) {
      var go = countUp(el);
      if (!go) return;
      if (io) { el._count = go; io.observe(el); } else go(); // démarre quand la carte est visible
    });
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

  /* ---------- Bandeau du tableau de bord : anneau d'une couleur secondaire tirée au hasard à chaque arrivée ---------- */
  var RINGS = ['magenta', 'turquoise', 'bleu', 'vertclair', 'jaune', 'orange', 'vert']; // violet et bleu nuit : trop peu visibles sur le bleu UGE
  var lastRing = null;
  function initRing() {
    if (document.documentElement.classList.contains('figma')) return; // import Figma : magenta stable (styles.css)
    $$('.hero.compact').forEach(function (h) {
      var pool = RINGS.filter(function (c) { return c !== lastRing; });
      lastRing = pool[Math.floor(Math.random() * pool.length)];
      h.style.setProperty('--ring', 'var(--c-' + lastRing + ')');
    });
  }

  function init() {
    $$('.rate').forEach(function (r) { setRate(r, parseInt(r.getAttribute('data-value') || '0', 10)); });
    initRole();
    initCounters();
    initRing();
    $$('.stops-field').forEach(syncStops);
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
