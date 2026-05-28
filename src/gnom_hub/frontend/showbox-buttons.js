/* showbox-buttons.js — Modular Showbox Button Controller */

(function () {
  const ShowboxButtons = {
    buttons: {
      'prev': { id: 'sb-btn-prev', text: '', icon: '', disabled: false, color: '', onClick: null },
      'delete': { id: 'sb-btn-delete', text: '', icon: '', disabled: false, color: '', onClick: null },
      'switch': { id: 'sb-btn-switch', text: '', icon: '', disabled: false, color: '', onClick: null },
      'next': { id: 'sb-btn-next', text: '', icon: '', disabled: false, color: '', onClick: null },
      'cancel': { id: 'sb-btn-cancel', text: '', icon: '', disabled: true, color: '', onClick: null },
      'ok': { id: 'sb-btn-ok', text: '', icon: '', disabled: true, color: '', onClick: null }
    },

    init() {
      Object.keys(this.buttons).forEach(key => {
        const btnConf = this.buttons[key];
        const el = document.getElementById(btnConf.id);
        if (el) {
          const newEl = el.cloneNode(true);
          el.parentNode.replaceChild(newEl, el);
          newEl.addEventListener('click', (e) => {
            e.stopPropagation();
            if (btnConf.onClick && !btnConf.disabled) {
              btnConf.onClick(e);
            }
          });
        }
      });
      this.renderAll();
    },

    configure(key, config) {
      if (!this.buttons[key]) return;
      this.buttons[key] = { ...this.buttons[key], ...config };
      this.render(key);
    },

    render(key) {
      const btnConf = this.buttons[key];
      const el = document.getElementById(btnConf.id);
      if (!el) return;

      el.disabled = btnConf.disabled;
      el.style.opacity = btnConf.disabled ? '0.4' : '1';
      el.style.pointerEvents = btnConf.disabled ? 'none' : 'auto';

      el.className = 'sb-btn';
      if (key === 'cancel' || key === 'ok') {
        el.classList.add('sb-btn-long');
      }
      if (btnConf.color) {
        el.classList.add(`sb-btn-${btnConf.color}`);
      }

      let html = '';
      if (btnConf.icon) {
        html += btnConf.icon;
      }
      if (btnConf.text) {
        if (html) html += ' ';
        html += `<span>${btnConf.text}</span>`;
      }
      el.innerHTML = html || '&nbsp;';
    },

    renderAll() {
      Object.keys(this.buttons).forEach(key => this.render(key));
    }
  };

  window.ShowboxButtons = ShowboxButtons;
})();
