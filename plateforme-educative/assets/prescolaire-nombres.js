/* Paliers de plateforme choisis par la propriétaire, pas des seuils ministériels. */
(() => {
  'use strict';
  const age = Number(document.body.dataset.numberAge);
  const bands = age === 5
    ? [['1-10', 1, 10], ['11-20', 11, 20], ['21-31', 21, 31], ['1-31', 1, 31]]
    : [['1-5', 1, 5], ['6-10', 6, 10], ['11-15', 11, 15], ['1-15', 1, 15]];
  const storageKey = `club${age}-nombres-palier-v1`;
  let stored;
  try { stored = JSON.parse(localStorage.getItem(storageKey)); } catch {}
  let band = bands.find(b => b[0] === stored) || bands[0];
  const field = document.createElement('fieldset');
  field.className = 'number-levels wood';
  const legend = document.createElement('legend');
  legend.textContent = 'Choisis tes nombres';
  field.append(legend);
  const label = document.createElement('label');
  label.htmlFor = 'number-band'; label.textContent = 'Mon palier : ';
  const select = document.createElement('select'); select.id = 'number-band';
  for (const b of bands) {
    const option = document.createElement('option'); option.value = b[0];
    option.textContent = `${b === bands.at(-1) ? 'Tout mélanger : ' : ''}${b[1]} à ${b[2]}`;
    select.append(option);
  }
  select.value = band[0]; label.append(select); field.append(label);
  const note = document.createElement('p'); note.className = 'help-note';
  note.textContent = 'Commence par le premier palier. Explore les suivants quand tu en as envie, avec un adulte au besoin.';
  field.append(note); document.querySelector('.club-task').before(field);
  select.addEventListener('change', () => {
    band = bands.find(b => b[0] === select.value) || bands[0];
    try { localStorage.setItem(storageKey, JSON.stringify(band[0])); } catch {}
    start();
  });
  window.CLUB_NUMBERS = {
    get min() { return band[1]; }, get max() { return band[2]; },
    get key() { return band[0]; }, get age() { return age; },
    values() { return Array.from({ length: band[2] - band[1] + 1 }, (_, i) => band[1] + i); }
  };
})();
