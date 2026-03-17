/**
 * QUANTEX — Scroll Animations & Intersection Observer
 * Upravljanje animacijama na skrolu
 */

(function () {
  'use strict';

  /* ── Intersection Observer za scroll animacije ──────────── */
  function initScrollAnimations() {
    const elements = document.querySelectorAll('.animate-on-scroll');
    if (!elements.length) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('in-view');
            // Prati animaciju koraka u procesu
            if (entry.target.classList.contains('process-step')) {
              entry.target.classList.add('in-view');
            }
            observer.unobserve(entry.target);
          }
        });
      },
      {
        threshold: 0.12,
        rootMargin: '0px 0px -60px 0px'
      }
    );

    elements.forEach((el, index) => {
      // Stagger delay na osnovu animationDelay atributa ili indeksa
      const existingDelay = parseFloat(el.style.animationDelay) || 0;
      if (!existingDelay && el.style.transitionDelay === '') {
        el.style.transitionDelay = `${(index % 4) * 0.04}s`;
      }
      observer.observe(el);
    });
  }

  /* ── Numerički brojač za hero statistike ────────────────── */
  function initHeroCounters() {
    const counters = document.querySelectorAll('.stat-number[data-target]');
    if (!counters.length) return;

    const observerOpts = {
      threshold: 0.5,
      rootMargin: '0px'
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const el = entry.target;
          const target = parseInt(el.getAttribute('data-target'), 10);
          if (isNaN(target)) return;

          animateHeroCounter(el, target, 1600);
          observer.unobserve(el);
        }
      });
    }, observerOpts);

    counters.forEach(counter => observer.observe(counter));
  }

  function animateHeroCounter(el, target, duration) {
    const startTime = performance.now();

    function easeOutQuart(t) {
      return 1 - Math.pow(1 - t, 4);
    }

    function update(now) {
      const elapsed = now - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const value = Math.round(easeOutQuart(progress) * target);
      el.textContent = value;
      if (progress < 1) {
        requestAnimationFrame(update);
      } else {
        el.textContent = target;
      }
    }

    requestAnimationFrame(update);
  }

  /* ── Sticky nav ─────────────────────────────────────────── */
  function initStickyNav() {
    const header = document.getElementById('site-header');
    if (!header) return;

    let lastScrollY = window.scrollY;
    let ticking = false;

    function updateNav() {
      const scrollY = window.scrollY;

      if (scrollY > 20) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }

      lastScrollY = scrollY;
      ticking = false;
    }

    window.addEventListener('scroll', () => {
      if (!ticking) {
        requestAnimationFrame(updateNav);
        ticking = true;
      }
    }, { passive: true });

    // Inicijalni poziv
    updateNav();
  }

  /* ── Active nav link na skrolu ──────────────────────────── */
  function initActiveNavLinks() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');
    if (!sections.length || !navLinks.length) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            navLinks.forEach(link => link.classList.remove('active'));
            const activeLink = document.querySelector(`.nav-link[href="#${entry.target.id}"]`);
            if (activeLink) activeLink.classList.add('active');
          }
        });
      },
      {
        rootMargin: '-40% 0px -40% 0px',
        threshold: 0
      }
    );

    sections.forEach(section => observer.observe(section));
  }

  /* ── Back to top dugme ──────────────────────────────────── */
  function initBackToTop() {
    const btn = document.getElementById('backToTop');
    if (!btn) return;

    let ticking = false;

    function updateButton() {
      if (window.scrollY > 400) {
        btn.removeAttribute('hidden');
        btn.classList.add('visible');
      } else {
        btn.classList.remove('visible');
        setTimeout(() => {
          if (!btn.classList.contains('visible')) {
            btn.setAttribute('hidden', '');
          }
        }, 300);
      }
      ticking = false;
    }

    window.addEventListener('scroll', () => {
      if (!ticking) {
        requestAnimationFrame(updateButton);
        ticking = true;
      }
    }, { passive: true });

    btn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* ── Page load progress bar ─────────────────────────────── */
  function initProgressBar() {
    const bar = document.createElement('div');
    bar.className = 'page-progress';
    bar.setAttribute('role', 'progressbar');
    bar.setAttribute('aria-hidden', 'true');
    bar.style.width = '0%';
    document.body.prepend(bar);

    let ticking = false;

    function updateProgress() {
      const scrollTop = window.scrollY;
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
      bar.style.width = `${Math.min(progress, 100)}%`;
      ticking = false;
    }

    window.addEventListener('scroll', () => {
      if (!ticking) {
        requestAnimationFrame(updateProgress);
        ticking = true;
      }
    }, { passive: true });
  }

  /* ── Copyright year ─────────────────────────────────────── */
  function initCopyrightYear() {
    const yearEl = document.getElementById('copyright-year');
    if (yearEl) {
      yearEl.textContent = new Date().getFullYear();
    }
  }

  /* ── Paralelni entry animacije za karticee ──────────────── */
  function initServiceCardStagger() {
    const cards = document.querySelectorAll('.service-card.animate-on-scroll');
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry, i) => {
          if (entry.isIntersecting) {
            const delay = parseInt(entry.target.style.animationDelay) || i * 80;
            entry.target.style.transitionDelay = `${delay}ms`;
            entry.target.classList.add('in-view');
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
    );
    cards.forEach(card => observer.observe(card));
  }

  /* ── Init All ───────────────────────────────────────────── */
  function init() {
    // Proveri da li je Intersection Observer podržan
    if (!('IntersectionObserver' in window)) {
      // Fallback: prikaži sve odmah
      document.querySelectorAll('.animate-on-scroll').forEach(el => {
        el.classList.add('in-view');
      });
      return;
    }

    initScrollAnimations();
    initHeroCounters();
    initStickyNav();
    initActiveNavLinks();
    initBackToTop();
    initProgressBar();
    initCopyrightYear();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

}());
