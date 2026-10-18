const CACHE_NAME = 'fieldnotes-__CACHE_VERSION__';
const CACHE_PREFIX = 'fieldnotes-';
const ICONS = ['/assets/icon-192.png', '/assets/icon-512.png'];

function contentType(path) {
  if (path.endsWith('.html') || path === '/') return 'text/html; charset=utf-8';
  if (path.endsWith('.css')) return 'text/css; charset=utf-8';
  if (path.endsWith('.js')) return 'text/javascript; charset=utf-8';
  if (path.endsWith('.webmanifest')) return 'application/manifest+json; charset=utf-8';
  return 'application/json; charset=utf-8';
}

self.addEventListener('install', event => {
  event.waitUntil((async () => {
    const response = await fetch('/offline-pack.json', { cache: 'no-store' });
    if (!response.ok) throw new Error('Offline notes could not be downloaded');
    const files = await response.json();
    const cache = await caches.open(CACHE_NAME);
    const entries = Object.entries(files);
    try {
      for (let index = 0; index < entries.length; index += 16) {
        await Promise.all(entries.slice(index, index + 16).map(([path, body]) =>
          cache.put(path, new Response(body, { headers: { 'Content-Type': contentType(path) } }))
        ));
      }
      await cache.addAll(ICONS);
      await self.skipWaiting();
    } catch (error) {
      await caches.delete(CACHE_NAME);
      throw error;
    }
  })());
});

self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    const names = await caches.keys();
    await Promise.all(names.filter(name => name.startsWith(CACHE_PREFIX) && name !== CACHE_NAME).map(name => caches.delete(name)));
    await self.clients.claim();
  })());
});

self.addEventListener('fetch', event => {
  const request = event.request;
  const url = new URL(request.url);
  if (request.method !== 'GET' || url.origin !== self.location.origin || url.pathname === '/offline-pack.json') return;

  event.respondWith((async () => {
    const cache = await caches.open(CACHE_NAME);
    try {
      const response = await fetch(request);
      if (response.ok) await cache.put(request, response.clone());
      return response;
    } catch {
      const saved = await cache.match(request, { ignoreSearch: true });
      if (saved) return saved;
      if (request.mode === 'navigate') {
        return new Response('<!doctype html><html lang="en"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Offline | Fieldnotes</title><body style="font:16px Arial,sans-serif;padding:2rem;max-width:36rem"><h1>Page not saved</h1><p>Connect to the internet to open this page.</p><p><a href="/">Go to Fieldnotes</a></p></body></html>', { headers: { 'Content-Type': 'text/html; charset=utf-8' }, status: 503 });
      }
      return Response.error();
    }
  })());
});
