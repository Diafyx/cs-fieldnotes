const dialog = document.getElementById('search-dialog');
const input = document.getElementById('search-input');
const results = document.getElementById('search-results');
let catalog;

function readTheme() {
  try { return localStorage.getItem('fieldnotes-theme'); } catch { return null; }
}

function saveTheme(value) {
  try { localStorage.setItem('fieldnotes-theme', value); } catch { /* Local storage may be disabled. */ }
}

function setTheme(value) {
  document.documentElement.dataset.theme = value;
  saveTheme(value);
}

setTheme(readTheme() || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'));
document.querySelector('[data-theme-toggle]').addEventListener('click', () => {
  setTheme(document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark');
});

function displayResults(query) {
  results.replaceChildren();
  if (!catalog) return;
  const words = query.trim().toLowerCase().split(/\s+/).filter(Boolean);
  if (!words.length) {
    const hint = document.createElement('p');
    hint.className = 'search-empty';
    hint.textContent = 'Type a concept, course name, or subject.';
    results.append(hint);
    return;
  }
  const matches = catalog.map(item => {
    const title = item.title.toLowerCase();
    const haystack = `${title} ${item.course.toLowerCase()} ${item.subject}`;
    if (!words.every(word => haystack.includes(word))) return null;
    const score = (title.startsWith(query.toLowerCase()) ? 10 : 0) + (item.ready ? 2 : 0);
    return { item, score };
  }).filter(Boolean).sort((a, b) => b.score - a.score || a.item.title.localeCompare(b.item.title)).slice(0, 30);
  if (!matches.length) {
    const empty = document.createElement('p');
    empty.className = 'search-empty';
    empty.textContent = 'No matching topics in the inventory.';
    results.append(empty);
    return;
  }
  for (const { item } of matches) {
    const link = document.createElement('a');
    link.className = 'search-result';
    link.href = item.url;
    const title = document.createElement('span');
    title.textContent = item.title;
    const meta = document.createElement('small');
    meta.textContent = item.ready ? item.course : `${item.course} / planned`;
    link.append(title, meta);
    results.append(link);
  }
}

async function openSearch() {
  dialog.showModal();
  input.focus();
  if (!catalog) {
    try {
      const response = await fetch('/catalog.json');
      if (!response.ok) throw new Error('Catalog could not be loaded');
      catalog = await response.json();
    } catch {
      results.textContent = 'Search is unavailable. Use the subject pages to browse topics.';
      return;
    }
  }
  displayResults(input.value);
}

document.querySelector('[data-open-search]').addEventListener('click', openSearch);
document.querySelector('[data-close-search]').addEventListener('click', () => dialog.close());
input.addEventListener('input', () => displayResults(input.value));
dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
document.addEventListener('keydown', event => {
  if (event.key === '/' && !dialog.open && !['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) {
    event.preventDefault();
    openSearch();
  }
});

const offlineStatus = document.querySelector('[data-offline-status]');
if ('serviceWorker' in navigator) {
  window.addEventListener('load', async () => {
    try {
      const registration = await navigator.serviceWorker.register('/sw.js', { updateViaCache: 'none' });
      const updateStatus = () => {
        if (!offlineStatus) return;
        if (registration.active || navigator.serviceWorker.controller) {
          offlineStatus.textContent = 'Notes ready for offline reading.';
        } else if (registration.installing || registration.waiting) {
          offlineStatus.textContent = 'Saving notes for offline reading. Keep this page open.';
        } else {
          offlineStatus.textContent = 'Open this page online to save the notes.';
        }
      };
      updateStatus();
      registration.installing?.addEventListener('statechange', updateStatus);
      registration.addEventListener('updatefound', () => {
        updateStatus();
        registration.installing?.addEventListener('statechange', updateStatus);
      });
      navigator.serviceWorker.addEventListener('controllerchange', updateStatus);
    } catch {
      if (offlineStatus) offlineStatus.textContent = 'Offline notes are unavailable in this browser.';
    }
  });
} else if (offlineStatus) {
  offlineStatus.textContent = 'Offline notes are unavailable in this browser.';
}

const installButton = document.querySelector('[data-install-app]');
let installPrompt;
window.addEventListener('beforeinstallprompt', event => {
  if (!installButton) return;
  event.preventDefault();
  installPrompt = event;
  installButton.hidden = false;
});
installButton?.addEventListener('click', async () => {
  if (!installPrompt) return;
  installPrompt.prompt();
  await installPrompt.userChoice;
  installPrompt = null;
  installButton.hidden = true;
});
window.addEventListener('appinstalled', () => {
  if (installButton) installButton.hidden = true;
});
