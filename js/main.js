/**
 * QUANTEX — Main JS
 * Navigacija, FAQ accordion, forma, smooth scroll, pomoćne funkcije
 */

(function () {
  'use strict';

  /* ── Dropdown Navigation ────────────────────────────────── */
  function initDropdowns() {
    const triggers = document.querySelectorAll('.nav-dropdown-trigger');

    triggers.forEach(trigger => {
      const dropdown = document.getElementById(trigger.getAttribute('aria-controls'));
      if (!dropdown) return;

      function openDropdown() {
        trigger.setAttribute('aria-expanded', 'true');
        dropdown.classList.add('dropdown-open');
      }

      function closeDropdown() {
        trigger.setAttribute('aria-expanded', 'false');
        dropdown.classList.remove('dropdown-open');
      }

      trigger.addEventListener('click', (e) => {
        e.stopPropagation();
        const isOpen = trigger.getAttribute('aria-expanded') === 'true';
        // Zatvori sve ostale
        document.querySelectorAll('.nav-dropdown-trigger').forEach(t => {
          if (t !== trigger) {
            t.setAttribute('aria-expanded', 'false');
            const d = document.getElementById(t.getAttribute('aria-controls'));
            if (d) d.classList.remove('dropdown-open');
          }
        });
        isOpen ? closeDropdown() : openDropdown();
      });

      // Zatvori na klik izvan
      document.addEventListener('click', (e) => {
        if (!trigger.contains(e.target) && !dropdown.contains(e.target)) {
          closeDropdown();
        }
      });

      // Keyboard: Escape zatvara
      dropdown.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
          closeDropdown();
          trigger.focus();
        }
      });

      // Hover za desktop
      if (window.matchMedia('(hover: hover)').matches) {
        const parent = trigger.closest('.nav-item');
        if (parent) {
          parent.addEventListener('mouseenter', openDropdown);
          parent.addEventListener('mouseleave', closeDropdown);
        }
      }
    });
  }

  /* ── Mobile Navigation ──────────────────────────────────── */
  function initMobileNav() {
    const toggle   = document.getElementById('navToggle');
    const navMenu  = document.getElementById('navMenu');
    const navLinks = navMenu ? navMenu.querySelectorAll('a') : [];

    if (!toggle || !navMenu) return;

    function openMenu() {
      navMenu.classList.add('nav-open');
      toggle.setAttribute('aria-expanded', 'true');
      toggle.setAttribute('aria-label', 'Zatvori meni');
      document.body.style.overflow = 'hidden';
    }

    function closeMenu() {
      navMenu.classList.remove('nav-open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.setAttribute('aria-label', 'Otvori meni');
      document.body.style.overflow = '';
    }

    toggle.addEventListener('click', () => {
      const isOpen = navMenu.classList.contains('nav-open');
      isOpen ? closeMenu() : openMenu();
    });

    // Zatvori meni na klik linka
    navLinks.forEach(link => {
      link.addEventListener('click', () => {
        if (window.innerWidth < 768) closeMenu();
      });
    });

    // Zatvori meni na klik izvan menija
    document.addEventListener('click', (e) => {
      if (
        navMenu.classList.contains('nav-open') &&
        !navMenu.contains(e.target) &&
        !toggle.contains(e.target)
      ) {
        closeMenu();
      }
    });

    // Zatvori meni na Escape
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && navMenu.classList.contains('nav-open')) {
        closeMenu();
        toggle.focus();
      }
    });

    // Zatvori meni pri resize
    window.addEventListener('resize', () => {
      if (window.innerWidth >= 768) closeMenu();
    }, { passive: true });
  }

  /* ── FAQ Accordion ──────────────────────────────────────── */
  function initFAQ() {
    const faqItems = document.querySelectorAll('.faq-item');
    if (!faqItems.length) return;

    faqItems.forEach(item => {
      const question = item.querySelector('.faq-question');
      const answer   = item.querySelector('.faq-answer');

      if (!question || !answer) return;

      question.addEventListener('click', () => {
        const isExpanded = question.getAttribute('aria-expanded') === 'true';

        // Zatvori sve ostale
        faqItems.forEach(other => {
          if (other === item) return;
          const otherQ = other.querySelector('.faq-question');
          const otherA = other.querySelector('.faq-answer');
          if (otherQ && otherA) {
            otherQ.setAttribute('aria-expanded', 'false');
            collapseAnswer(otherA);
          }
        });

        // Toggle current
        if (isExpanded) {
          question.setAttribute('aria-expanded', 'false');
          collapseAnswer(answer);
        } else {
          question.setAttribute('aria-expanded', 'true');
          expandAnswer(answer);
        }
      });

      // Keyboard navigation
      question.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowDown') {
          e.preventDefault();
          const nextItem = item.nextElementSibling;
          const nextQ = nextItem ? nextItem.querySelector('.faq-question') : null;
          if (nextQ) nextQ.focus();
        }
        if (e.key === 'ArrowUp') {
          e.preventDefault();
          const prevItem = item.previousElementSibling;
          const prevQ = prevItem ? prevItem.querySelector('.faq-question') : null;
          if (prevQ) prevQ.focus();
        }
        if (e.key === 'Home') {
          e.preventDefault();
          const firstQ = document.querySelector('.faq-question');
          if (firstQ) firstQ.focus();
        }
        if (e.key === 'End') {
          e.preventDefault();
          const allQ = document.querySelectorAll('.faq-question');
          if (allQ.length) allQ[allQ.length - 1].focus();
        }
      });
    });
  }

  function expandAnswer(el) {
    el.removeAttribute('hidden');
    el.classList.add('opening');

    // Animacija visine
    el.style.height = '0';
    el.style.overflow = 'hidden';
    el.style.transition = 'height 0.3s cubic-bezier(0.22, 1, 0.36, 1)';

    requestAnimationFrame(() => {
      const targetH = el.scrollHeight;
      el.style.height = targetH + 'px';
    });

    el.addEventListener('transitionend', function handler() {
      el.style.height = '';
      el.style.overflow = '';
      el.style.transition = '';
      el.classList.remove('opening');
      el.removeEventListener('transitionend', handler);
    });
  }

  function collapseAnswer(el) {
    el.style.height = el.scrollHeight + 'px';
    el.style.overflow = 'hidden';
    el.style.transition = 'height 0.25s ease';

    requestAnimationFrame(() => {
      el.style.height = '0';
    });

    el.addEventListener('transitionend', function handler() {
      el.setAttribute('hidden', '');
      el.style.height = '';
      el.style.overflow = '';
      el.style.transition = '';
      el.removeEventListener('transitionend', handler);
    });
  }

  /* ── Contact Form ───────────────────────────────────────── */
  function initContactForm() {
    const form       = document.getElementById('contactForm');
    const successMsg = document.getElementById('formSuccess');
    if (!form) return;

    const fields = {
      name:    { el: document.getElementById('cf-name'),    msg: 'Unesite vaše ime i prezime.' },
      company: { el: document.getElementById('cf-company'), msg: 'Unesite naziv vaše kompanije.' },
      email:   { el: document.getElementById('cf-email'),   msg: 'Unesite ispravnu email adresu.' }
    };

    function validateEmail(email) {
      return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    function setFieldError(fieldEl, errorMsg) {
      fieldEl.classList.add('has-error');
      const errSpan = fieldEl.parentElement.querySelector('.form-error');
      if (errSpan) errSpan.textContent = errorMsg;
    }

    function clearFieldError(fieldEl) {
      fieldEl.classList.remove('has-error');
      const errSpan = fieldEl.parentElement.querySelector('.form-error');
      if (errSpan) errSpan.textContent = '';
    }

    // Real-time validation
    Object.values(fields).forEach(({ el }) => {
      if (!el) return;
      el.addEventListener('blur', () => validateField(el));
      el.addEventListener('input', () => clearFieldError(el));
    });

    function validateField(el) {
      if (!el) return true;
      const key = el.name;
      if (!el.value.trim()) {
        setFieldError(el, fields[key]?.msg || 'Ovo polje je obavezno.');
        return false;
      }
      if (key === 'email' && !validateEmail(el.value.trim())) {
        setFieldError(el, 'Unesite ispravnu email adresu.');
        return false;
      }
      clearFieldError(el);
      return true;
    }

    function validateAll() {
      let valid = true;
      Object.values(fields).forEach(({ el }) => {
        if (!validateField(el)) valid = false;
      });
      return valid;
    }

    function setSubmitLoading(btn, loading) {
      if (loading) {
        btn.disabled = true;
        btn.dataset.originalText = btn.innerHTML;
        btn.innerHTML = `
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true" style="animation: spin 0.8s linear infinite">
            <path d="M21 12a9 9 0 11-6-8.5"/>
          </svg>
          Slanje...
        `;
      } else {
        btn.disabled = false;
        btn.innerHTML = btn.dataset.originalText || 'Zakažite razgovor';
      }
    }

    form.addEventListener('submit', (e) => {
      e.preventDefault();

      if (!validateAll()) {
        const firstError = form.querySelector('.has-error');
        if (firstError) firstError.focus();
        return;
      }

      const submitBtn = form.querySelector('.form-submit-btn');
      setSubmitLoading(submitBtn, true);

      const formData = new FormData(form);
      fetch('https://api.web3forms.com/submit', {
        method: 'POST',
        body: formData
      })
        .then(res => res.json())
        .then(data => {
          setSubmitLoading(submitBtn, false);
          if (data.success) {
            form.reset();
            if (successMsg) {
              successMsg.removeAttribute('hidden');
              successMsg.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
            setTimeout(() => {
              if (successMsg) successMsg.setAttribute('hidden', '');
            }, 6000);
            if (typeof window.gtag === 'function') {
              window.gtag('event', 'contact_form_submit', {
                event_category: 'conversion',
                event_label: 'schedule_meeting'
              });
            }
          } else {
            setSubmitLoading(submitBtn, false);
            alert('Greška pri slanju. Molimo pokušajte ponovo ili nas kontaktirajte direktno.');
          }
        })
        .catch(() => {
          setSubmitLoading(submitBtn, false);
          alert('Greška pri slanju. Proverite internet konekciju i pokušajte ponovo.');
        });
    });
  }

  /* ── Smooth Scroll za navigacione linkove ───────────────── */
  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', (e) => {
        const href = anchor.getAttribute('href');
        if (!href || href === '#') return;

        const target = document.querySelector(href);
        if (!target) return;

        e.preventDefault();

        const headerH = document.getElementById('site-header')?.offsetHeight || 72;
        const targetTop = target.getBoundingClientRect().top + window.scrollY - headerH - 16;

        window.scrollTo({
          top: Math.max(0, targetTop),
          behavior: 'smooth'
        });

        // Focus management za pristupačnost
        target.setAttribute('tabindex', '-1');
        target.focus({ preventScroll: true });
        target.addEventListener('blur', () => target.removeAttribute('tabindex'), { once: true });
      });
    });
  }

  /* ── Hover paralax efekat na service kartice ────────────── */
  function initCardTilt() {
    // Samo na uređajima koji podržavaju hover (ne touch)
    if (window.matchMedia('(hover: none)').matches) return;

    const cards = document.querySelectorAll('.service-card');

    cards.forEach(card => {
      card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = (e.clientX - rect.left) / rect.width - 0.5;
        const y = (e.clientY - rect.top) / rect.height - 0.5;

        card.style.transform = `
          perspective(1000px)
          rotateX(${-y * 3}deg)
          rotateY(${x * 3}deg)
          translateY(-3px)
        `;
      });

      card.addEventListener('mouseleave', () => {
        card.style.transform = '';
      });
    });
  }

  /* ── Lazy loading za slike ──────────────────────────────── */
  function initLazyImages() {
    if (!('IntersectionObserver' in window)) return;

    const images = document.querySelectorAll('img[data-src]');
    if (!images.length) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src;
          img.removeAttribute('data-src');
          observer.unobserve(img);
        }
      });
    }, { rootMargin: '200px' });

    images.forEach(img => observer.observe(img));
  }

  /* ── Skip link ──────────────────────────────────────────── */
  function initSkipLink() {
    const skipLink = document.createElement('a');
    skipLink.href = '#main-content';
    skipLink.className = 'skip-link';
    skipLink.textContent = 'Preskoči na sadržaj';
    skipLink.style.cssText = `
      position: fixed;
      top: -100%;
      left: 16px;
      padding: 12px 20px;
      background: var(--accent);
      color: white;
      font-weight: 600;
      font-size: 14px;
      border-radius: 0 0 8px 8px;
      z-index: 9999;
      transition: top 0.2s;
      text-decoration: none;
    `;

    skipLink.addEventListener('focus', () => {
      skipLink.style.top = '0';
    });

    skipLink.addEventListener('blur', () => {
      skipLink.style.top = '-100%';
    });

    document.body.prepend(skipLink);
  }

  /* ── Testimonials Slider ────────────────────────────────── */
  function initTestimonialsSlider() {
    const section = document.getElementById('recenzije');
    if (!section) return;
    const cards = Array.from(section.querySelectorAll('.testimonial-card'));
    if (cards.length < 4) return;

    const PER_PAGE = 4;
    const groupCount = Math.ceil(cards.length / PER_PAGE);

    // Build DOM
    const slider = document.createElement('div');
    slider.className = 'testimonials-slider';

    const track = document.createElement('div');
    track.className = 'testimonials-track';
    slider.appendChild(track);

    for (let i = 0; i < groupCount; i++) {
      const group = document.createElement('div');
      group.className = 'slide-group';
      cards.slice(i * PER_PAGE, (i + 1) * PER_PAGE).forEach(c => {
        c.classList.remove('animate-on-scroll');
        c.removeAttribute('style');
        group.appendChild(c);
      });
      track.appendChild(group);
    }

    const controls = document.createElement('div');
    controls.className = 'slider-controls';
    controls.innerHTML = `
      <button class="slider-btn slider-prev" aria-label="Prethodna stranica">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 18l-6-6 6-6"/></svg>
      </button>
      <div class="slider-dots"></div>
      <button class="slider-btn slider-next" aria-label="Sledeća stranica">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18l6-6-6-6"/></svg>
      </button>`;
    slider.appendChild(controls);

    const grid = section.querySelector('.testimonials-grid');
    grid.parentNode.replaceChild(slider, grid);

    const dotsWrap = controls.querySelector('.slider-dots');
    const dots = [];
    for (let i = 0; i < groupCount; i++) {
      const dot = document.createElement('button');
      dot.className = 'slider-dot' + (i === 0 ? ' active' : '');
      dot.setAttribute('aria-label', 'Stranica ' + (i + 1));
      dot.addEventListener('click', () => { goTo(i); startAuto(); });
      dotsWrap.appendChild(dot);
      dots.push(dot);
    }

    let current = 0;
    let autoTimer;

    function goTo(index) {
      current = ((index % groupCount) + groupCount) % groupCount;
      track.style.transform = 'translateX(-' + (current * slider.offsetWidth) + 'px)';
      dots.forEach((d, i) => d.classList.toggle('active', i === current));
    }

    function startAuto() {
      clearInterval(autoTimer);
      autoTimer = setInterval(() => goTo(current + 1), 5000);
    }

    controls.querySelector('.slider-prev').addEventListener('click', () => { goTo(current - 1); startAuto(); });
    controls.querySelector('.slider-next').addEventListener('click', () => { goTo(current + 1); startAuto(); });

    slider.addEventListener('mouseenter', () => clearInterval(autoTimer));
    slider.addEventListener('mouseleave', startAuto);

    let resizeTimer;
    window.addEventListener('resize', () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(() => goTo(current), 150);
    });

    startAuto();
  }

  /* ── Init All ───────────────────────────────────────────── */
  function init() {
    initDropdowns();
    initMobileNav();
    initFAQ();
    initContactForm();
    initSmoothScroll();
    initCardTilt();
    initLazyImages();
    initSkipLink();
    initTestimonialsSlider();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

}());
