/**
 * BDU İmtahana Giriş Balı Hesablama - Application Logic
 * Clean, modular JavaScript for score calculation
 * Author: BDU Calculator Team
 * License: MIT
 */

(function() {
  'use strict';

  // ========================================
  // Configuration & Constants
  // ========================================
  const CONFIG = {
    HOURS_PENALTY: {
      HIGH: 0.33,   // 60+ hours: 0.33 per absence
      LOW: 0.5      // 15-45 hours: 0.5 per absence
    },
    HOURS_THRESHOLD: 60,
    MAX_ATTENDANCE: 10,
    MAX_SCORE: 50,
    WEIGHTS: {
      COLLOQUIUM: 0.6,
      SEMINAR: 0.4
    },
    STORAGE_KEY: 'bdu-calculator-theme'
  };

  // ========================================
  // DOM Elements Cache
  // ========================================
  const elements = {
    form: null,
    themeToggle: null,
    seminarCountSelect: null,
    seminarInputsContainer: null,
    resultsCard: null,
    resultElements: {}
  };

  // ========================================
  // Theme Management
  // ========================================
  const ThemeManager = {
    init() {
      const savedTheme = localStorage.getItem(CONFIG.STORAGE_KEY);
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      
      if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
        document.body.classList.add('dark');
        this.updateToggleIcon(true);
      }
    },

    toggle() {
      const isDark = document.body.classList.toggle('dark');
      localStorage.setItem(CONFIG.STORAGE_KEY, isDark ? 'dark' : 'light');
      this.updateToggleIcon(isDark);
    },

    updateToggleIcon(isDark) {
      if (elements.themeToggle) {
        const icon = elements.themeToggle.querySelector('.theme-icon');
        const text = elements.themeToggle.querySelector('.theme-text');
        if (icon) icon.textContent = isDark ? '☀️' : '🌙';
        if (text) text.textContent = isDark ? 'Açıq rejim' : 'Tünd rejim';
      }
    }
  };

  // ========================================
  // Seminar Input Generator
  // ========================================
  const SeminarManager = {
    generate(count) {
      const container = elements.seminarInputsContainer;
      if (!container) return;

      container.innerHTML = '';
      
      if (count < 1 || count > 10) return;

      const grid = document.createElement('div');
      grid.className = 'form-grid form-grid--3cols';

      for (let i = 1; i <= count; i++) {
        const group = document.createElement('div');
        group.className = 'form-group';
        
        group.innerHTML = `
          <label class="form-label" for="seminar${i}">
            ${i}-ci seminar
          </label>
          <input 
            type="number" 
            id="seminar${i}" 
            class="form-input seminar-input" 
            min="0" 
            max="10" 
            step="0.1" 
            placeholder="0-10"
            aria-label="${i}-ci seminar balı"
            required
          >
        `;
        
        grid.appendChild(group);
      }

      container.appendChild(grid);
    },

    getScores() {
      const inputs = document.querySelectorAll('.seminar-input');
      const scores = [];
      let valid = true;

      inputs.forEach(input => {
        const value = parseFloat(input.value);
        if (isNaN(value) || value < 0 || value > 10 || input.value.trim() === '') {
          input.classList.add('error');
          valid = false;
        } else {
          input.classList.remove('error');
          scores.push(value);
        }
      });

      return { valid, scores };
    }
  };

  // ========================================
  // Form Validation
  // ========================================
  const Validator = {
    validateNumber(value, min, max) {
      const num = parseFloat(value);
      return !isNaN(num) && num >= min && num <= max;
    },

    validateRequired(element) {
      if (!element.value || element.value.trim() === '') {
        element.classList.add('error');
        return false;
      }
      element.classList.remove('error');
      return true;
    },

    validateRadioGroup(name) {
      const selected = document.querySelector(`input[name="${name}"]:checked`);
      return selected !== null;
    },

    showError(elementId, message) {
      const errorEl = document.getElementById(`${elementId}-error`);
      if (errorEl) {
        errorEl.textContent = message;
        errorEl.classList.add('visible');
      }
    },

    hideError(elementId) {
      const errorEl = document.getElementById(`${elementId}-error`);
      if (errorEl) {
        errorEl.classList.remove('visible');
      }
    },

    clearAllErrors() {
      document.querySelectorAll('.form-error').forEach(el => el.classList.remove('visible'));
      document.querySelectorAll('.form-input.error, .form-select.error').forEach(el => el.classList.remove('error'));
    }
  };

  // ========================================
  // Score Calculator
  // ========================================
  const Calculator = {
    calculate(data) {
      // Colloquium: average * 0.6
      const collAvg = (data.coll1 + data.coll2 + data.coll3) / 3;
      const collScore = collAvg * CONFIG.WEIGHTS.COLLOQUIUM;

      // Seminar: average * 0.4
      const seminarAvg = data.seminars.length > 0 
        ? data.seminars.reduce((a, b) => a + b, 0) / data.seminars.length 
        : 0;
      const seminarScore = seminarAvg * CONFIG.WEIGHTS.SEMINAR;

      // Attendance: 10 - (absences * penalty)
      const penalty = data.courseHours >= CONFIG.HOURS_THRESHOLD 
        ? CONFIG.HOURS_PENALTY.HIGH 
        : CONFIG.HOURS_PENALTY.LOW;
      let attendanceScore = CONFIG.MAX_ATTENDANCE - (data.absences * penalty);
      attendanceScore = Math.max(0, Math.min(CONFIG.MAX_ATTENDANCE, attendanceScore));

      // Independent work (direct score)
      const independentScore = data.independentWork;

      // Total (capped at MAX_SCORE)
      let totalScore = collScore + seminarScore + attendanceScore + independentScore;
      totalScore = Math.min(CONFIG.MAX_SCORE, totalScore);

      // Scale conversion if needed
      const scale = data.resultScale;
      const displayScore = scale === 10 ? totalScore / 5 : totalScore;

      return {
        colloquium: { average: collAvg, weighted: collScore },
        seminar: { average: seminarAvg, weighted: seminarScore },
        attendance: attendanceScore,
        independent: independentScore,
        total: totalScore,
        display: displayScore,
        scale: scale
      };
    }
  };

  // ========================================
  // Results Display
  // ========================================
  const ResultsDisplay = {
    show(results) {
      const card = elements.resultsCard;
      if (!card) return;

      // Update individual result values
      this.updateValue('resultColl', 
        `${results.colloquium.weighted.toFixed(2)} (ort: ${results.colloquium.average.toFixed(2)})`);
      this.updateValue('resultSem', 
        `${results.seminar.weighted.toFixed(2)} (ort: ${results.seminar.average.toFixed(2)})`);
      this.updateValue('resultAtt', results.attendance.toFixed(2));
      this.updateValue('resultInd', results.independent.toFixed(2));
      
      // Update final score display
      const finalValue = document.getElementById('finalScoreValue');
      const finalLabel = document.getElementById('finalScoreLabel');
      
      if (finalValue) {
        finalValue.textContent = `${results.display.toFixed(2)} / ${results.scale}`;
      }
      if (finalLabel) {
        finalLabel.textContent = 'İmtahana Giriş Balı';
      }

      // Show the card with animation
      card.classList.remove('hidden');
      card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    },

    hide() {
      if (elements.resultsCard) {
        elements.resultsCard.classList.add('hidden');
      }
    },

    updateValue(id, value) {
      const el = document.getElementById(id);
      if (el) el.textContent = value;
    }
  };

  // ========================================
  // Form Handler
  // ========================================
  const FormHandler = {
    init() {
      elements.form = document.getElementById('calculatorForm');
      elements.themeToggle = document.getElementById('themeToggle');
      elements.seminarCountSelect = document.getElementById('seminarCount');
      elements.seminarInputsContainer = document.getElementById('seminarInputsContainer');
      elements.resultsCard = document.getElementById('resultsCard');

      this.bindEvents();
      
      // Initialize with default seminar count
      if (elements.seminarCountSelect) {
        SeminarManager.generate(parseInt(elements.seminarCountSelect.value) || 3);
      }
    },

    bindEvents() {
      // Form submission
      if (elements.form) {
        elements.form.addEventListener('submit', (e) => {
          e.preventDefault();
          this.handleSubmit();
        });
      }

      // Theme toggle
      if (elements.themeToggle) {
        elements.themeToggle.addEventListener('click', () => {
          ThemeManager.toggle();
        });
      }

      // Seminar count change
      if (elements.seminarCountSelect) {
        elements.seminarCountSelect.addEventListener('change', (e) => {
          const count = parseInt(e.target.value) || 0;
          SeminarManager.generate(count);
        });
      }

      // Reset button
      const resetBtn = document.getElementById('resetBtn');
      if (resetBtn) {
        resetBtn.addEventListener('click', () => this.reset());
      }

      // Input validation on blur
      document.querySelectorAll('.form-input, .form-select').forEach(input => {
        input.addEventListener('blur', () => {
          if (input.value) {
            Validator.validateRequired(input);
          }
        });
      });
    },

    handleSubmit() {
      Validator.clearAllErrors();

      // Gather form data
      const courseHoursEl = document.querySelector('input[name="courseHours"]:checked');
      const resultScaleEl = document.querySelector('input[name="resultScale"]:checked');

      if (!courseHoursEl) {
        alert('Zəhmət olmasa dərs saatını seçin.');
        return;
      }

      const coll1 = parseFloat(document.getElementById('coll1')?.value);
      const coll2 = parseFloat(document.getElementById('coll2')?.value);
      const coll3 = parseFloat(document.getElementById('coll3')?.value);
      const independentWork = parseFloat(document.getElementById('independentWork')?.value);
      const absences = parseInt(document.getElementById('absences')?.value) || 0;

      // Validate colloquium scores
      if (isNaN(coll1) || isNaN(coll2) || isNaN(coll3)) {
        alert('Zəhmət olmasa bütün kollekvium ballarını daxil edin (0-10 arası).');
        return;
      }

      // Validate seminar scores
      const seminarData = SeminarManager.getScores();
      if (!seminarData.valid || seminarData.scores.length === 0) {
        alert('Zəhmət olmasa bütün seminar ballarını düzgün daxil edin (0-10 arası).');
        return;
      }

      // Validate independent work
      if (isNaN(independentWork) || independentWork < 0 || independentWork > 10) {
        alert('Zəhmət olmasa sərbəst iş balını daxil edin (0-10 arası).');
        return;
      }

      // Calculate
      const data = {
        courseHours: parseInt(courseHoursEl.value),
        resultScale: parseInt(resultScaleEl?.value) || 50,
        coll1, coll2, coll3,
        seminars: seminarData.scores,
        independentWork,
        absences
      };

      const results = Calculator.calculate(data);
      ResultsDisplay.show(results);
    },

    reset() {
      if (elements.form) {
        elements.form.reset();
      }
      ResultsDisplay.hide();
      Validator.clearAllErrors();
      
      // Re-generate default seminar inputs
      if (elements.seminarCountSelect) {
        SeminarManager.generate(3);
      }
      
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  // ========================================
  // Initialization
  // ========================================
  function init() {
    ThemeManager.init();
    FormHandler.init();
    
    console.log('BDU Calculator initialized successfully.');
  }

  // Run on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
