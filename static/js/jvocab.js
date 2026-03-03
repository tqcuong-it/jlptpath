// Japanese Vocab Highlight — Click to show reading + meaning + pronunciation
(function () {
  let activePopup = null;

  function closePopup() {
    if (activePopup) {
      activePopup.remove();
      activePopup = null;
    }
  }

  function speak(text) {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const u = new SpeechSynthesisUtterance(text);
      u.lang = 'ja-JP';
      u.rate = 0.85;
      window.speechSynthesis.speak(u);
    }
  }

  function showPopup(el) {
    closePopup();

    const word = el.textContent.trim();
    const reading = el.dataset.reading || '';
    const meaning = el.dataset.meaning || '';

    const popup = document.createElement('div');
    popup.className = 'jvocab-popup';
    popup.innerHTML = `
      <div class="jvocab-popup-word">${word}</div>
      ${reading ? `<div class="jvocab-popup-reading">📖 ${reading}</div>` : ''}
      ${meaning ? `<div class="jvocab-popup-meaning">🇻🇳 ${meaning}</div>` : ''}
      <button class="jvocab-popup-speak" aria-label="Phát âm">🔊 Nghe</button>
    `;

    // Position popup
    const rect = el.getBoundingClientRect();
    popup.style.position = 'fixed';
    popup.style.zIndex = '9999';

    document.body.appendChild(popup);

    // Calculate position after render
    const popupRect = popup.getBoundingClientRect();
    let top = rect.top - popupRect.height - 8;
    let left = rect.left + (rect.width - popupRect.width) / 2;

    // Keep on screen
    if (top < 8) top = rect.bottom + 8;
    if (left < 8) left = 8;
    if (left + popupRect.width > window.innerWidth - 8) {
      left = window.innerWidth - popupRect.width - 8;
    }

    popup.style.top = top + 'px';
    popup.style.left = left + 'px';

    // Speak button
    popup.querySelector('.jvocab-popup-speak').addEventListener('click', (e) => {
      e.stopPropagation();
      speak(word);
    });

    // Auto-speak on open
    speak(word);

    activePopup = popup;
  }

  // Event delegation
  document.addEventListener('click', (e) => {
    const word = e.target.closest('.jvocab-word');
    if (word) {
      e.preventDefault();
      e.stopPropagation();
      showPopup(word);
      return;
    }
    if (!e.target.closest('.jvocab-popup')) {
      closePopup();
    }
  });

  // Keyboard support
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closePopup();
    if ((e.key === 'Enter' || e.key === ' ') && e.target.classList.contains('jvocab-word')) {
      e.preventDefault();
      showPopup(e.target);
    }
  });
})();
