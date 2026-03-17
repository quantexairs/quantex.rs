/**
 * QUANTEX — Time & Money Savings Calculator
 * Interaktivni kalkulator uštede za AI automatizaciju
 */

(function () {
  'use strict';

  /* ── DOM References ─────────────────────────────────────── */
  const employeeInput   = document.getElementById('calc-employees');
  const salaryInput     = document.getElementById('calc-salary');
  const hoursRange      = document.getElementById('calc-hours');
  const automationRange = document.getElementById('calc-automation');
  const hoursDisplay    = document.getElementById('hours-display');
  const automationDisplay = document.getElementById('automation-display');
  const calcBtn         = document.getElementById('calcBtn');
  const resultsContent  = document.getElementById('resultsContent');
  const resultsPlaceholder = document.getElementById('resultsPlaceholder');
  const resultHours     = document.getElementById('result-hours');
  const resultFTE       = document.getElementById('result-fte');
  const resultMoney     = document.getElementById('result-money');
  const resultROI       = document.getElementById('result-roi');
  const resultMonthlyCost = document.getElementById('result-monthly-cost');

  /* ── Constants ──────────────────────────────────────────── */
  const WORKING_HOURS_MONTH = 168;   // prosek radnih sati mesečno
  const WORKING_WEEKS_YEAR  = 50;    // radne nedelje godišnje
  const HOURS_PER_FTE_YEAR  = 1920;  // sati pune zaposlenosti godišnje

  // Okvirni troškovi implementacije (RSD) na osnovu broja zaposlenih
  const IMPL_COST_BASE   = 250000;
  const IMPL_COST_PER_EMP = 25000;
  const IMPL_COST_MAX    = 3500000;

  /* ── Utility: Format number for Serbian locale ──────────── */
  function formatNumber(n) {
    if (n >= 1000000) {
      return (n / 1000000).toFixed(1).replace('.', ',') + ' mil.';
    }
    return Math.round(n).toLocaleString('sr-RS');
  }

  /* ── Utility: Animate counter ───────────────────────────── */
  function animateCounter(el, targetValue, duration, formatter) {
    if (!el) return;

    const startTime = performance.now();
    const startValue = 0;
    const fmt = formatter || formatNumber;

    // Easing function (ease out cubic)
    function easeOutCubic(t) {
      return 1 - Math.pow(1 - t, 3);
    }

    function update(currentTime) {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const eased = easeOutCubic(progress);
      const current = Math.round(startValue + (targetValue - startValue) * eased);

      el.textContent = fmt(current);

      if (progress < 1) {
        requestAnimationFrame(update);
      } else {
        el.textContent = fmt(targetValue);
      }
    }

    requestAnimationFrame(update);
  }

  /* ── Core Calculation Logic ─────────────────────────────── */
  function calculate() {
    const employees   = Math.max(1, parseInt(employeeInput.value) || 1);
    const salary      = Math.max(30000, parseInt(salaryInput.value) || 120000);
    const hoursWeekly = Math.max(2, parseInt(hoursRange.value) || 12);
    const autoRate    = Math.max(30, parseInt(automationRange.value) || 65) / 100;

    // Ukupni radni sati na repetitivnim zadacima (godišnje)
    const totalRepetitiveHoursYear = employees * hoursWeekly * WORKING_WEEKS_YEAR;

    // Sati koji mogu biti automatizovani
    const savedHours = Math.round(totalRepetitiveHoursYear * autoRate);

    // FTE ekvivalent
    const fteEquivalent = (savedHours / HOURS_PER_FTE_YEAR).toFixed(1);

    // Troškovna vrednost: satnica = mesečna plata / radni sati mesečno
    const hourlyRate = salary / WORKING_HOURS_MONTH;

    // Mesečni trošak repetitivnog rada po timu
    const monthlyRepetitiveCost = Math.round(
      employees * hoursWeekly * 4.33 * hourlyRate
    );

    // Godišnja finansijska vrednost uštede
    const annualSavedMoney = Math.round(totalRepetitiveHoursYear * autoRate * hourlyRate);

    // Procena troška implementacije
    const implCost = Math.min(
      IMPL_COST_BASE + (employees * IMPL_COST_PER_EMP),
      IMPL_COST_MAX
    );

    // ROI period u mesecima (zaokruživanje na gore)
    const monthlyBenefit = annualSavedMoney / 12;
    const roiMonths = monthlyBenefit > 0
      ? Math.ceil(implCost / monthlyBenefit)
      : 0;

    return {
      savedHours,
      fteEquivalent,
      annualSavedMoney,
      roiMonths: Math.min(roiMonths, 36), // cap na 36 meseci radi realizma
      monthlyRepetitiveCost
    };
  }

  /* ── Display Results ────────────────────────────────────── */
  function displayResults(data) {
    const ANIM_DURATION = 1200;

    // Prikaži rezultate, sakrij placeholder
    resultsPlaceholder.style.display = 'none';
    resultsContent.removeAttribute('hidden');
    resultsContent.classList.add('entering');

    setTimeout(() => resultsContent.classList.remove('entering'), 600);

    // Animirani brojevi
    animateCounter(resultHours, data.savedHours, ANIM_DURATION, formatNumber);
    animateCounter(resultMoney, data.annualSavedMoney, ANIM_DURATION, formatNumber);
    animateCounter(resultROI, data.roiMonths, ANIM_DURATION, (n) => String(Math.round(n)));
    animateCounter(resultMonthlyCost, data.monthlyRepetitiveCost, ANIM_DURATION, formatNumber);

    // FTE (plain string)
    if (resultFTE) {
      resultFTE.textContent = data.fteEquivalent;
    }

    // Skroluj do rezultata na mobilnim
    if (window.innerWidth < 900) {
      setTimeout(() => {
        resultsContent.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 200);
    }
  }

  /* ── Range Slider: real-time display ───────────────────────*/
  function bindRangeDisplay(rangeEl, displayEl, suffix) {
    if (!rangeEl || !displayEl) return;

    function updateDisplay() {
      displayEl.textContent = rangeEl.value + suffix;
      // Update ARIA value
      rangeEl.setAttribute('aria-valuenow', rangeEl.value);
      // Update gradient fill
      const min = parseFloat(rangeEl.min);
      const max = parseFloat(rangeEl.max);
      const val = parseFloat(rangeEl.value);
      const pct = ((val - min) / (max - min)) * 100;
      rangeEl.style.background =
        `linear-gradient(90deg, var(--accent) 0%, var(--cyan) ${pct}%, rgba(255,255,255,0.08) ${pct}%)`;
    }

    rangeEl.addEventListener('input', updateDisplay);
    updateDisplay(); // Initial state
  }

  /* ── Input Validation ───────────────────────────────────── */
  function validateInputs() {
    let valid = true;

    if (!employeeInput.value || parseInt(employeeInput.value) < 1) {
      employeeInput.style.borderColor = 'rgba(239,68,68,0.5)';
      employeeInput.focus();
      valid = false;
    } else {
      employeeInput.style.borderColor = '';
    }

    if (!salaryInput.value || parseInt(salaryInput.value) < 30000) {
      salaryInput.style.borderColor = 'rgba(239,68,68,0.5)';
      if (valid) salaryInput.focus();
      valid = false;
    } else {
      salaryInput.style.borderColor = '';
    }

    return valid;
  }

  /* ── Button State ───────────────────────────────────────── */
  function setButtonLoading(loading) {
    if (!calcBtn) return;
    if (loading) {
      calcBtn.disabled = true;
      calcBtn.innerHTML = `
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true" style="animation: spin 0.8s linear infinite">
          <path d="M21 12a9 9 0 11-6-8.5"/>
        </svg>
        Izračunavam...
      `;
    } else {
      calcBtn.disabled = false;
      calcBtn.innerHTML = `
        Izračunaj uštedu
        <svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
      `;
    }
  }

  /* ── Main Handler ───────────────────────────────────────── */
  function handleCalculate() {
    if (!validateInputs()) return;

    setButtonLoading(true);

    // Simulacija kratkog procesiranja za UX
    setTimeout(() => {
      const data = calculate();
      displayResults(data);
      setButtonLoading(false);

      // Track event (ako postoji analytics)
      if (typeof window.gtag === 'function') {
        window.gtag('event', 'calculator_used', {
          event_category: 'engagement',
          event_label: 'savings_calculator'
        });
      }
    }, 600);
  }

  /* ── Init ───────────────────────────────────────────────── */
  function init() {
    if (!calcBtn) return;

    // Bind range sliders
    bindRangeDisplay(hoursRange, hoursDisplay, 'h');
    bindRangeDisplay(automationRange, automationDisplay, '%');

    // Button click
    calcBtn.addEventListener('click', handleCalculate);

    // Enter key on number inputs
    [employeeInput, salaryInput].forEach(input => {
      if (!input) return;
      input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') handleCalculate();
      });
      // Clear error on input
      input.addEventListener('input', () => {
        input.style.borderColor = '';
      });
    });

    // Formatuj salary input na blur
    if (salaryInput) {
      salaryInput.addEventListener('blur', () => {
        const val = parseInt(salaryInput.value);
        if (val && val >= 30000) {
          salaryInput.value = val;
        }
      });
    }
  }

  // CSS za spin animaciju
  const style = document.createElement('style');
  style.textContent = `@keyframes spin { to { transform: rotate(360deg); } }`;
  document.head.appendChild(style);

  // Inicijalizacija kada DOM bude spreman
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

}());
