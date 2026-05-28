/* showbox-buttons.js — Modular Showbox Button Controller */

(function () {
  const ShowboxButtons = {
    buttons: {
      'prev': { id: 'sb-btn-prev', text: '', icon: 'prev', disabled: false, color: '', onClick: null },
      'delete': { id: 'sb-btn-delete', text: '', icon: 'delete', disabled: false, color: '', onClick: null },
      'switch': { id: 'sb-btn-switch', text: '', icon: 'switch', disabled: false, color: '', onClick: null },
      'next': { id: 'sb-btn-next', text: '', icon: 'next', disabled: false, color: '', onClick: null },
      'cancel': { id: 'sb-btn-cancel', text: 'Abbrechen', icon: '', disabled: true, color: 'red', onClick: null },
      'ok': { id: 'sb-btn-ok', text: 'Okay', icon: '', disabled: true, color: 'green', onClick: null }
    },

    icons: {
      prev: `<svg viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle;"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>`,
      delete: `<svg viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle;"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>`,
      switch: `<svg viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle;"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline></svg>`,
      next: `<svg viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle;"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>`
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
      if (btnConf.disabled) {
        el.style.opacity = '0.4';
        el.style.pointerEvents = 'none';
      } else {
        el.style.opacity = '1';
        el.style.pointerEvents = 'auto';
      }

      el.className = 'sb-btn';
      if (key === 'cancel' || key === 'ok') {
        el.classList.add('sb-btn-long');
      }
      if (btnConf.color) {
        el.classList.add(`sb-btn-${btnConf.color}`);
      }

      let html = '';
      if (btnConf.icon && this.icons[btnConf.icon]) {
        html += this.icons[btnConf.icon];
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
