// Japanese Vocab Highlight — Click to show reading + meaning + type + pronunciation
(function () {
  'use strict';
  let activePopup = null;

  function closePopup() {
    if (activePopup) { activePopup.remove(); activePopup = null; }
  }

  function speak(text) {
    if (!('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text);
    u.lang = 'ja-JP';
    u.rate = 0.85;
    const voices = window.speechSynthesis.getVoices();
    const jaVoice = voices.find(v => v.lang === 'ja-JP') || voices.find(v => v.lang.startsWith('ja'));
    if (jaVoice) u.voice = jaVoice;
    window.speechSynthesis.speak(u);
  }

  function showPopup(el) {
    closePopup();
    const word = el.textContent.trim();
    const reading = el.dataset.reading || '';
    const meaning = el.dataset.meaning || '';
    const type = el.dataset.type || '';

    const popup = document.createElement('div');
    popup.className = 'jvocab-popup';
    popup.style.position = 'fixed';
    popup.style.zIndex = '9999';

    let html = '<div class="jvocab-popup-word">' + word + '</div>';
    if (reading) html += '<div class="jvocab-popup-reading">📖 ' + reading + '</div>';
    if (type) html += '<div class="jvocab-popup-type" style="font-size:.78rem;color:var(--secondary);margin-bottom:4px;font-style:italic">(' + type + ')</div>';
    if (meaning) html += '<div class="jvocab-popup-meaning">🇻🇳 ' + meaning + '</div>';
    html += '<button class="jvocab-popup-speak" aria-label="Phát âm">🔊 Nghe phát âm</button>';

    popup.innerHTML = html;
    document.body.appendChild(popup);

    const rect = el.getBoundingClientRect();
    const popupRect = popup.getBoundingClientRect();
    let top = rect.top - popupRect.height - 8;
    let left = rect.left + (rect.width - popupRect.width) / 2;
    if (top < 8) top = rect.bottom + 8;
    if (left < 8) left = 8;
    if (left + popupRect.width > window.innerWidth - 8) left = window.innerWidth - popupRect.width - 8;
    popup.style.top = top + 'px';
    popup.style.left = left + 'px';

    popup.querySelector('.jvocab-popup-speak').addEventListener('click', function(e) {
      e.stopPropagation();
      speak(word);
    });

    speak(word);
    activePopup = popup;
  }

  document.addEventListener('click', function(e) {
    var word = e.target.closest('.jvocab-word');
    if (word) { e.preventDefault(); e.stopPropagation(); showPopup(word); return; }
    if (!e.target.closest('.jvocab-popup')) closePopup();
  });

  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') closePopup();
    if ((e.key === 'Enter' || e.key === ' ') && e.target.classList.contains('jvocab-word')) {
      e.preventDefault();
      showPopup(e.target);
    }
  });

  if ('speechSynthesis' in window) {
    window.speechSynthesis.getVoices();
    window.speechSynthesis.onvoiceschanged = function() { window.speechSynthesis.getVoices(); };
  }
})();
