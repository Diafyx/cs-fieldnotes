const dialog = document.getElementById('search-dialog');
const input = document.getElementById('search-input');
const results = document.getElementById('search-results');
const bundledAndroidApp = location.hostname === 'appassets.androidplatform.net';
let catalog;
const searchHistoryKey = 'fieldnotes-recent-searches';

function recentSearches() {
  try {
    const saved = JSON.parse(localStorage.getItem(searchHistoryKey));
    return Array.isArray(saved) ? saved.filter(value => typeof value === 'string').slice(0, 5) : [];
  } catch { return []; }
}

function rememberSearch(value) {
  const query = value.trim().replace(/\s+/g, ' ').slice(0, 120);
  if (!query) return;
  const history = [query, ...recentSearches().filter(item => item.toLowerCase() !== query.toLowerCase())].slice(0, 5);
  try { localStorage.setItem(searchHistoryKey, JSON.stringify(history)); } catch { /* Local storage may be disabled. */ }
}

function readTheme() {
  try { return localStorage.getItem('fieldnotes-theme'); } catch { return null; }
}

function saveTheme(value) {
  try { localStorage.setItem('fieldnotes-theme', value); } catch { /* Local storage may be disabled. */ }
}

function setTheme(value) {
  document.documentElement.dataset.theme = value;
  saveTheme(value);
  if (bundledAndroidApp) fetch(`/__app_theme__/${value}`).catch(() => {});
}

setTheme(readTheme() || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'));
document.querySelector('[data-theme-toggle]').addEventListener('click', () => {
  setTheme(document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark');
});

const subjectNav = document.querySelector('.side-nav');
if (subjectNav && matchMedia('(max-width: 900px)').matches) {
  const key = 'fieldnotes-subject-nav-scroll';
  try {
    const saved = Number(sessionStorage.getItem(key));
    if (Number.isFinite(saved) && saved > 0) subjectNav.scrollLeft = saved;
  } catch { /* Session storage may be disabled. */ }

  const selected = subjectNav.querySelector('.nav-link.active');
  if (selected) {
    const navBox = subjectNav.getBoundingClientRect();
    const selectedBox = selected.getBoundingClientRect();
    if (selectedBox.right > navBox.right) subjectNav.scrollLeft += selectedBox.right - navBox.right + 8;
    if (selectedBox.left < navBox.left) subjectNav.scrollLeft -= navBox.left - selectedBox.left + 8;
  }

  const saveSubjectNav = () => {
    try { sessionStorage.setItem(key, String(subjectNav.scrollLeft)); } catch { /* Session storage may be disabled. */ }
  };
  subjectNav.addEventListener('scroll', saveSubjectNav);
  subjectNav.addEventListener('click', event => {
    if (event.target.closest('a')) saveSubjectNav();
  });
  window.addEventListener('pagehide', saveSubjectNav);
}

const modules = [...document.querySelectorAll('details.module')];
if (modules.length) {
  const key = `fieldnotes-modules:${location.pathname}`;
  const names = modules.map(module => module.querySelector('summary')?.textContent.trim());
  try {
    const saved = JSON.parse(sessionStorage.getItem(key));
    if (Array.isArray(saved) && saved.length === modules.length &&
        saved.every((item, index) => item.name === names[index] && typeof item.open === 'boolean')) {
      modules.forEach((module, index) => { module.open = saved[index].open; });
    }
  } catch { /* Session storage may be disabled. */ }

  const saveModules = () => {
    try {
      sessionStorage.setItem(key, JSON.stringify(modules.map((module, index) => ({
        name: names[index], open: module.open
      }))));
    } catch { /* Session storage may be disabled. */ }
  };
  modules.forEach(module => module.addEventListener('toggle', saveModules));
  window.addEventListener('pagehide', saveModules);
}

function displayResults(query) {
  results.replaceChildren();
  const words = query.trim().toLowerCase().split(/\s+/).filter(Boolean);
  if (!words.length) {
    const history = recentSearches();
    if (history.length) {
      const heading = document.createElement('div');
      heading.className = 'search-history-heading';
      const label = document.createElement('span');
      label.textContent = 'Recent searches';
      const clear = document.createElement('button');
      clear.type = 'button';
      clear.textContent = 'Clear';
      clear.addEventListener('click', () => {
        try { localStorage.removeItem(searchHistoryKey); } catch { /* Local storage may be disabled. */ }
        displayResults('');
      });
      heading.append(label, clear);
      results.append(heading);
      for (const search of history) {
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'search-history-item';
        button.textContent = search;
        button.addEventListener('click', () => {
          input.value = search;
          input.focus();
          displayResults(search);
        });
        results.append(button);
      }
      return;
    }
    const hint = document.createElement('p');
    hint.className = 'search-empty';
    hint.textContent = 'Type a concept, course name, or subject.';
    results.append(hint);
    return;
  }
  if (!catalog) return;
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
  input.value = '';
  displayResults('');
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
input.addEventListener('keydown', event => {
  if (event.key === 'Enter') rememberSearch(input.value);
});
results.addEventListener('click', event => {
  if (event.target.closest('a.search-result')) rememberSearch(input.value);
});
dialog.addEventListener('close', () => rememberSearch(input.value));
dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
document.addEventListener('keydown', event => {
  if (event.key === '/' && !dialog.open && !['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) {
    event.preventDefault();
    openSearch();
  }
});

const offlineStatus = document.querySelector('[data-offline-status]');
if (!bundledAndroidApp && 'serviceWorker' in navigator) {
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
} else if (offlineStatus && !bundledAndroidApp) {
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
