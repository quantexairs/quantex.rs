/**
 * QUANTEX — Time & Money Savings Calculator
 * Supports both SR (RSD) and EN (EUR) modes via html[lang]
 */

(function () {
  'use strict';

  const IS_EN = document.documentElement.lang === 'en';

  /* ── DOM References ─────────────────────────────────────── */
  const employeeInput     = document.getElementById('calc-employees');
  const salaryInput       = document.getElementById('calc-salary');
  const hoursRange        = document.getElementById('calc-hours');
  const automationRange   = document.getElementById('calc-automation');
  const serviceSelect     = document.getElementById('calc-service');
  const hoursDisplay      = document.getElementById('hours-display');
  const automationDisplay = document.getElementById('automation-display');
  const calcBtn           = document.getElementById('calcBtn');
  const resultsContent    = document.getElementById('resultsContent');
  const resultsPlaceholder = document.getElementById('resultsPlaceholder');
  const resultHours       = document.getElementById('result-hours');
  const resultFTE         = document.getElementById('result-fte');
  const resultMoney       = document.getElementById('result-money');
  const resultROI         = document.getElementById('result-roi');
  const resultMonthlyCost = document.getElementById('result-monthly-cost');

  /* ── Constants ──────────────────────────────────────────── */
  const WORKING_HOURS_MONTH = 168;
  const WORKING_WEEKS_YEAR  = 50;
  const HOURS_PER_FTE_YEAR  = 1920;

  // Service package costs (in EUR — converted to RSD when needed)
  const SERVICE_COSTS_EUR = {
    'scheduling-starter': { setup: 290,  monthly: 59  },
    'scheduling-pro':     { setup: 590,  monthly: 99  },
    'lead-starter':       { setup: 390,  monthly: 99  },
    'lead-pro':           { setup: 790,  monthly: 179 },
    'agent-starter':      { setup: 490,  monthly: 79  },
    'agent-pro':          { setup: 990,  monthly: 149 },
    'internal-starter':   { setup: 590,  monthly: 89  },
    'internal-pro':       { setup: 1190, monthly: 169 },
  };

  // Fallback formula constants (in EUR)
  const IMPL_COST_BASE_EUR    = 400;
  const IMPL_COST_PER_EMP_EUR = 40;
  const IMPL_COST_MAX_EUR     = 15000;

  // Exchange rate for RSD display
  const EUR_TO_RSD = 117;

  const SALARY_MIN = IS_EN ? 500 : 30000;

  /* ── Utility: Format number ─────────────────────────────── */
  function formatNumber(n) {
    if (IS_EN) {
      if (n >= 1000000) return (n / 1000000).toFixed(1) + 'M';
      if (n >= 1000)    return (n / 1000).toFixed(1) + 'k';
      return Math.round(n).toString();
    }
    if (n >= 1000000) return (n / 1000000).toFixed(1).replace('.', ',') + ' mil.';
    return Math.round(n).toLocaleString('sr-RS');
  }

  /* ── Utility: Animate counter ───────────────────────────── */
  function animateCounter(el, targetValue, duration, formatter) {
    if (!el) return;
    const startTime = performance.now();
    const fmt = formatter || formatNumber;

    function easeOutCubic(t) { return 1 - Math.pow(1 - t, 3); }

    function update(currentTime) {
      const elapsed  = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const current  = Math.round((targetValue) * easeOutCubic(progress));
      el.textContent = fmt(current);
      if (progress < 1) requestAnimationFrame(update);
      else el.textContent = fmt(targetValue);
    }

    requestAnimationFrame(update);
  }

  /* ── Core Calculation Logic ─────────────────────────────── */
  function calculate() {
    const employees   = Math.max(1, parseInt(employeeInput.value) || 1);
    const salary      = Math.max(SALARY_MIN, parseFloat(salaryInput.value) || (IS_EN ? 1500 : 120000));
    const hoursWeekly = Math.max(2, parseInt(hoursRange.value) || 12);
    const autoRate    = Math.max(30, parseInt(automationRange.value) || 65) / 100;

    // Convert salary to EUR for uniform calculation
    const salaryEUR = IS_EN ? salary : salary / EUR_TO_RSD;

    // Hourly rate (EUR)
    const hourlyRateEUR = salaryEUR / WORKING_HOURS_MONTH;

    // Repetitive hours per year
    const totalRepHoursYear = employees * hoursWeekly * WORKING_WEEKS_YEAR;
    const savedHours        = Math.round(totalRepHoursYear * autoRate);
    const fteEquivalent     = (savedHours / HOURS_PER_FTE_YEAR).toFixed(1);

    // Monthly repetitive cost (EUR)
    const monthlyRepCostEUR = employees * hoursWeekly * 4.33 * hourlyRateEUR;

    // Annual savings (EUR)
    const annualSavedEUR = totalRepHoursYear * autoRate * hourlyRateEUR;
    const monthlyBenefitEUR = annualSavedEUR / 12;

    // Implementation cost (EUR)
    let setupCostEUR    = 0;
    let monthlyRetainer = 0;

    const svc = serviceSelect && serviceSelect.value;
    if (svc && SERVICE_COSTS_EUR[svc]) {
      setupCostEUR    = SERVICE_COSTS_EUR[svc].setup;
      monthlyRetainer = SERVICE_COSTS_EUR[svc].monthly;
    } else {
      setupCostEUR = Math.min(
        IMPL_COST_BASE_EUR + employees * IMPL_COST_PER_EMP_EUR,
        IMPL_COST_MAX_EUR
      );
    }

    // Net monthly benefit after retainer
    const netMonthlyBenefitEUR = monthlyBenefitEUR - monthlyRetainer;
    const roiMonths = netMonthlyBenefitEUR > 0
      ? Math.ceil(setupCostEUR / netMonthlyBenefitEUR)
      : 99;

    // Convert to display currency
    const multiplier = IS_EN ? 1 : EUR_TO_RSD;

    return {
      savedHours,
      fteEquivalent,
      annualSavedMoney:    Math.round(annualSavedEUR    * multiplier),
      roiMonths:           Math.min(roiMonths, 36),
      monthlyRepetitiveCost: Math.round(monthlyRepCostEUR * multiplier),
    };
  }

  /* ── Display Results ────────────────────────────────────── */
  function displayResults(data) {
    const ANIM_DURATION = 1200;

    resultsPlaceholder.style.display = 'none';
    resultsContent.removeAttribute('hidden');
    resultsContent.classList.add('entering');
    setTimeout(() => resultsContent.classList.remove('entering'), 600);

    animateCounter(resultHours,       data.savedHours,             ANIM_DURATION, formatNumber);
    animateCounter(resultMoney,       data.annualSavedMoney,       ANIM_DURATION, formatNumber);
    animateCounter(resultROI,         data.roiMonths,              ANIM_DURATION, (n) => String(Math.round(n)));
    animateCounter(resultMonthlyCost, data.monthlyRepetitiveCost,  ANIM_DURATION, formatNumber);

    if (resultFTE) resultFTE.textContent = data.fteEquivalent;

    if (window.innerWidth < 900) {
      setTimeout(() => resultsContent.scrollIntoView({ behavior: 'smooth', block: 'start' }), 200);
    }
  }

  /* ── Range Slider: real-time display ───────────────────── */
  function bindRangeDisplay(rangeEl, displayEl, suffix) {
    if (!rangeEl || !displayEl) return;

    function updateDisplay() {
      displayEl.textContent = rangeEl.value + suffix;
      rangeEl.setAttribute('aria-valuenow', rangeEl.value);
      const min = parseFloat(rangeEl.min);
      const max = parseFloat(rangeEl.max);
      const pct = ((parseFloat(rangeEl.value) - min) / (max - min)) * 100;
      rangeEl.style.background =
        `linear-gradient(90deg, var(--accent) 0%, var(--cyan) ${pct}%, rgba(255,255,255,0.08) ${pct}%)`;
    }

    rangeEl.addEventListener('input', updateDisplay);
    updateDisplay();
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

    if (!salaryInput.value || parseFloat(salaryInput.value) < SALARY_MIN) {
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
    const spinnerSvg = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true" style="animation:spin 0.8s linear infinite"><path d="M21 12a9 9 0 11-6-8.5"/></svg>`;
    const arrowSvg   = `<svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>`;

    if (loading) {
      calcBtn.disabled = true;
      calcBtn.innerHTML = `${spinnerSvg} ${IS_EN ? 'Calculating...' : 'Izračunavam...'}`;
    } else {
      calcBtn.disabled = false;
      calcBtn.innerHTML = `${IS_EN ? 'Calculate savings' : 'Izračunaj uštedu'} ${arrowSvg}`;
    }
  }

  /* ── Main Handler ───────────────────────────────────────── */
  function handleCalculate() {
    if (!validateInputs()) return;

    setButtonLoading(true);

    setTimeout(() => {
      const data = calculate();
      displayResults(data);
      setButtonLoading(false);

      if (typeof window.gtag === 'function') {
        window.gtag('event', 'calculator_used', {
          event_category: 'engagement',
          event_label: 'savings_calculator',
        });
      }
    }, 600);
  }

  /* ── Init ───────────────────────────────────────────────── */
  function init() {
    if (!calcBtn) return;

    bindRangeDisplay(hoursRange,      hoursDisplay,      'h');
    bindRangeDisplay(automationRange, automationDisplay, '%');

    calcBtn.addEventListener('click', handleCalculate);

    [employeeInput, salaryInput].forEach(input => {
      if (!input) return;
      input.addEventListener('keydown', (e) => { if (e.key === 'Enter') handleCalculate(); });
      input.addEventListener('input',   () => { input.style.borderColor = ''; });
    });
  }

  // CSS for spin animation
  const style = document.createElement('style');
  style.textContent = `@keyframes spin { to { transform: rotate(360deg); } }`;
  document.head.appendChild(style);

  /* ── Calc Email Capture ─────────────────────────────────── */
  function initCalcEmail() {
    const emailForm = document.getElementById('calcEmailForm');
    const emailBtn  = document.getElementById('calcEmailBtn');
    const emailSent = document.getElementById('calcEmailSent');
    const reportField = document.getElementById('calcEmailReport');

    if (!emailForm) return;

    emailForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const emailVal = document.getElementById('calcEmailInput').value.trim();
      if (!emailVal) return;

      // Build report summary from current results
      const hours      = resultHours      ? resultHours.textContent      : '';
      const money      = resultMoney      ? resultMoney.textContent      : '';
      const roi        = resultROI        ? resultROI.textContent        : '';
      const monthly    = resultMonthlyCost? resultMonthlyCost.textContent: '';

      if (reportField) {
        reportField.value = `Godišnja ušteda sati: ${hours} | Finansijska vrednost: ${money} RSD | ROI period: ${roi} mes. | Mesečni trošak: ${monthly} RSD`;
      }

      emailBtn.disabled = true;
      emailBtn.textContent = 'Šaljem...';

      try {
        const fd = new FormData(emailForm);
        const res = await fetch('https://api.web3forms.com/submit', { method: 'POST', body: fd });
        const data = await res.json();
        if (data.success) {
          emailForm.style.display = 'none';
          emailSent.hidden = false;
          if (typeof window.gtag === 'function') {
            window.gtag('event', 'calc_email_sent', { event_category: 'lead', event_label: 'calculator_report' });
          }
        } else {
          emailBtn.disabled = false;
          emailBtn.textContent = 'Pošalji';
        }
      } catch {
        emailBtn.disabled = false;
        emailBtn.textContent = 'Pošalji';
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => { init(); initCalcEmail(); });
  } else {
    init();
    initCalcEmail();
  }

}());
