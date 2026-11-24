/* Quantex analytics: consent gate (Google Consent Mode v2), GA4 and PostHog.
 *
 * Nothing is requested from Google or PostHog before the visitor decides. The choice is kept for
 * 12 months in localStorage and can be changed from the footer link "Podešavanja kolačića".
 * PostHog stays off until POSTHOG_KEY below is filled in.
 *
 * Events (same names in GA4 and PostHog):
 *   cta_click          a link to the idea form (#ideja); props: location, label
 *   idea_form_started  first input into the idea form
 *   idea_submitted     the idea form was sent (GA4 key event)
 *   project_click      a link to one of the portfolio sites; props: project
 *   outbound_click     any other external link; props: host
 *   contact_click      mailto or tel link; props: kind
 *   faq_open           a FAQ question was opened; props: question
 *   video_play         an explainer video was started (once per page view); props: video (seo, aeo)
 *   video_complete     an explainer video played to the end; props: video
 * Any element can also carry data-track="event_name" and data-track-foo="bar".
 */
(function () {
  'use strict';

  var GA_ID = 'G-B0VB7R2391';
  var POSTHOG_KEY = 'phc_CYzhzujpWmHTDUmM9HpnciskRa5xi6rKEFC3vD3U6gMS'; // project API key (phc_...), public by design. Empty: PostHog is not loaded.
  var POSTHOG_HOST = 'https://eu.i.posthog.com';
  var SESSION_REPLAY = true; // recordings start only after consent; every input is masked
  var PROJECTS = ['3dlaboratorija.rs', 'angelicphoto.rs', 'relaxamassage.rs', 'autokodiranje.rs', 'thefreesecurity.com', 'antiquecroatia.com', 'elektricarpancevo.rs', 'astro7spell.in.rs'];
  var KEY = 'qx-consent';
  var LOCAL = /^(localhost|127\.0\.0\.1|\[::1\])$/.test(location.hostname) || location.protocol === 'file:';

  var loaded = false;
  var queue = [];

  window.dataLayer = window.dataLayer || [];
  window.gtag = function () { window.dataLayer.push(arguments); };
  window.gtag('consent', 'default', {
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied',
    analytics_storage: 'denied',
    functionality_storage: 'denied',
    personalization_storage: 'denied',
    security_storage: 'granted',
    wait_for_update: 500
  });

  function read() {
    try {
      var v = JSON.parse(localStorage.getItem(KEY) || 'null');
      if (!v || !v.ts || Date.now() - v.ts > 365 * 864e5) return null; // ask again after 12 months
      return { analytics: !!v.analytics, ts: v.ts };
    } catch (e) {
      return null;
    }
  }

  function send(event, props) {
    window.gtag('event', event, props);
    if (window.posthog && window.posthog.capture) window.posthog.capture(event, props);
  }

  function loadPosthog() {
    if (!POSTHOG_KEY || window.posthog) return;
    /* Official PostHog loader snippet. */
    !function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.crossOrigin="anonymous",p.async=!0,p.src=s.api_host.replace(".i.posthog.com","-assets.i.posthog.com")+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+".people (stub)"},o="init capture register register_once unregister opt_in_capturing opt_out_capturing has_opted_in_capturing has_opted_out_capturing identify reset startSessionRecording stopSessionRecording".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);
    window.posthog.init(POSTHOG_KEY, {
      api_host: POSTHOG_HOST,
      person_profiles: 'identified_only',
      persistence: 'localStorage+cookie',
      capture_pageview: true,
      capture_pageleave: true,
      autocapture: true,
      capture_performance: true,
      enable_heatmaps: true,
      disable_surveys: true,
      disable_session_recording: !SESSION_REPLAY,
      session_recording: { maskAllInputs: true, maskTextSelector: '[data-private]' }
    });
    if (LOCAL) window.posthog.register({ environment: 'local' });
  }

  function apply() {
    if (loaded) return;
    loaded = true;
    window.gtag('consent', 'update', { analytics_storage: 'granted', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied' });
    if (GA_ID && !LOCAL) {
      var s = document.createElement('script');
      s.async = true;
      s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(GA_ID);
      document.head.appendChild(s);
      window.gtag('js', new Date());
      window.gtag('config', GA_ID, { anonymize_ip: true, allow_google_signals: false, allow_ad_personalization_signals: false });
    }
    loadPosthog();
    queue.splice(0).forEach(function (q) { send(q[0], q[1]); });
  }

  window.qxTrack = function (event, props) {
    var c = read();
    if (!c || !c.analytics) return; // no consent, no tracking
    var full = { page: location.pathname };
    for (var k in props || {}) full[k] = props[k];
    if (!loaded) queue.push([event, full]);
    else send(event, full);
  };

  // ---------------------------------------------------------------- consent banner

  var banner = null;

  function buildBanner() {
    banner = document.createElement('section');
    banner.id = 'consent';
    banner.className = 'consent';
    banner.setAttribute('aria-labelledby', 'consent-title');
    banner.hidden = true;
    var policy = (document.querySelector('a[href$="politika-privatnosti.html"]') || {}).href || '/politika-privatnosti.html';
    banner.innerHTML =
      '<div class="consent-inner">' +
      '<div class="consent-copy"><h2 id="consent-title">Kolačići i merenje</h2>' +
      '<p>Uz tvoj pristanak merimo kako se sajt koristi, da bismo ga popravljali na osnovu podataka. Bez pristanka se ništa ne učitava. <a href="' + policy + '">Više u politici privatnosti</a></p></div>' +
      '<div class="consent-actions">' +
      '<button type="button" class="btn btn-secondary" data-consent="reject">Samo neophodno</button>' +
      '<button type="button" class="btn btn-primary" data-consent="accept">Prihvatam merenje</button>' +
      '</div></div>';
    document.body.appendChild(banner);
    banner.addEventListener('click', function (e) {
      var b = e.target.closest('[data-consent]');
      if (b) decide(b.getAttribute('data-consent') === 'accept');
    });
  }

  function show(open, focus) {
    if (!banner) buildBanner();
    banner.hidden = !open;
    if (open && focus) banner.querySelector('[data-consent="accept"]').focus({ preventScroll: true });
  }

  function decide(analytics) {
    var before = loaded;
    try {
      localStorage.setItem(KEY, JSON.stringify({ analytics: analytics, ts: Date.now() }));
    } catch (e) { /* storage blocked: the choice lasts for this page only */ }
    show(false);
    // Withdrawing a permission that was already in use: reload so that no tool keeps running.
    if (before && !analytics) { location.reload(); return; }
    if (analytics) apply();
  }

  window.qxConsent = { open: function () { show(true, true); }, get: read };

  // ---------------------------------------------------------------- automatic events

  function label(el) {
    return (el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 60);
  }

  function place(el) {
    var s = el.closest('header, footer, section, nav, main');
    if (!s) return 'page';
    return s.id || (s.className && String(s.className).split(' ')[0]) || s.tagName.toLowerCase();
  }

  document.addEventListener('click', function (e) {
    var t = e.target.closest ? e.target : null;
    if (!t) return;
    var open = t.closest('[data-consent-open]');
    if (open) { e.preventDefault(); show(true, true); return; }

    var tracked = t.closest('[data-track]');
    if (tracked) {
      var props = {};
      for (var k in tracked.dataset) if (k !== 'track' && k.indexOf('track') === 0 && tracked.dataset[k]) props[k.slice(5).toLowerCase()] = tracked.dataset[k];
      window.qxTrack(tracked.dataset.track, props);
    }

    var faq = t.closest('.faq-question');
    if (faq && faq.getAttribute('aria-expanded') !== 'true') window.qxTrack('faq_open', { question: label(faq) });

    var a = t.closest('a[href]');
    if (!a) return;
    var href = a.getAttribute('href') || '';
    if (/#ideja$/.test(href)) { window.qxTrack('cta_click', { location: place(a), label: label(a) }); return; }
    if (/^mailto:/i.test(href)) { window.qxTrack('contact_click', { kind: 'email' }); return; }
    if (/^tel:/i.test(href)) { window.qxTrack('contact_click', { kind: 'phone' }); return; }
    if (/^https?:/i.test(href) && a.hostname && a.hostname !== location.hostname) {
      var host = a.hostname.replace(/^www\./, '');
      if (PROJECTS.indexOf(host) >= 0) window.qxTrack('project_click', { project: host });
      else window.qxTrack('outbound_click', { host: host });
    }
  }, true);

  // Explainer videos: play and end do not bubble, so listen in the capture phase.
  var videoPlayed = {};
  document.addEventListener('play', function (e) {
    var v = e.target, id = v && v.getAttribute && v.getAttribute('data-video');
    if (!id || videoPlayed[id]) return;
    videoPlayed[id] = true;
    window.qxTrack('video_play', { video: id });
  }, true);
  document.addEventListener('ended', function (e) {
    var v = e.target, id = v && v.getAttribute && v.getAttribute('data-video');
    if (id) window.qxTrack('video_complete', { video: id });
  }, true);

  function ready() {
    var form = document.getElementById('contactForm');
    if (form) {
      var started = false;
      form.addEventListener('input', function () {
        if (started) return;
        started = true;
        window.qxTrack('idea_form_started');
      });
    }
    // Footer link to reopen the consent choice.
    var legal = document.querySelector('.footer-legal ul');
    if (legal && !document.querySelector('[data-consent-open]')) {
      var item = document.createElement('li');
      var link = document.createElement('a');
      link.href = '#';
      link.className = 'footer-link';
      link.setAttribute('data-consent-open', '');
      link.textContent = 'Podešavanja kolačića';
      item.appendChild(link);
      legal.appendChild(item);
    }
    var state = read();
    if (state && state.analytics) apply();
    else if (!state) show(true);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', ready);
  else ready();
})();
