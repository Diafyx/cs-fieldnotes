const CACHE_NAME = 'fieldnotes-__CACHE_VERSION__';
const CACHE_PREFIX = 'fieldnotes-';
const PACK_SHA256 = '__PACK_SHA256__';
const ASSET_HASHES = __ASSET_HASHES__;
const CSP = __CSP__;

async function sha256(bytes) {
  const digest = await crypto.subtle.digest('SHA-256', bytes);
  return Array.from(new Uint8Array(digest), byte => byte.toString(16).padStart(2, '0')).join('');
}

function contentType(path) {
  if (path.endsWith('.html') || path === '/') return 'text/html; charset=utf-8';
  if (path.endsWith('.css')) return 'text/css; charset=utf-8';
  if (path.endsWith('.js')) return 'text/javascript; charset=utf-8';
  if (path.endsWith('.webmanifest')) return 'application/manifest+json; charset=utf-8';
  return 'application/json; charset=utf-8';
}

function responseHeaders(path) {
  const headers = { 'Content-Type': contentType(path), 'X-Content-Type-Options': 'nosniff' };
  if (path.endsWith('.html') || path === '/') {
    headers['Content-Security-Policy'] = CSP;
    headers['X-Frame-Options'] = 'DENY';
    headers['Referrer-Policy'] = 'no-referrer';
    headers['Permissions-Policy'] = 'camera=(), microphone=(), geolocation=(), payment=(), usb=()';
  }
  return headers;
}

self.addEventListener('install', event => {
  event.waitUntil((async () => {
    const response = await fetch('/offline-pack.json', { cache: 'no-store' });
    if (!response.ok) throw new Error('Offline notes could not be downloaded');
    const bytes = await response.arrayBuffer();
    if (await sha256(bytes) !== PACK_SHA256) throw new Error('Offline notes did not match this app version');
    const files = JSON.parse(new TextDecoder().decode(bytes));
    const cache = await caches.open(CACHE_NAME);
    const entries = Object.entries(files);
    try {
      for (let index = 0; index < entries.length; index += 16) {
        await Promise.all(entries.slice(index, index + 16).map(([path, body]) =>
          cache.put(path, new Response(body, { headers: responseHeaders(path) }))
        ));
      }
      for (const [path, expectedHash] of Object.entries(ASSET_HASHES)) {
        const asset = await fetch(path, { cache: 'no-store' });
        if (!asset.ok) throw new Error(`Asset could not be downloaded: ${path}`);
        const data = await asset.arrayBuffer();
        if (await sha256(data) !== expectedHash) throw new Error(`Asset did not match this app version: ${path}`);
        await cache.put(path, new Response(data, { headers: { 'Content-Type': path.endsWith('.png') ? 'image/png' : 'font/ttf' } }));
      }
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
        return new Response('<!doctype html><html lang="en"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Offline | Fieldnotes</title><body><h1>Page not saved</h1><p>Connect to the internet to open this page.</p><p><a href="/">Go to Fieldnotes</a></p></body></html>', { headers: responseHeaders('/index.html'), status: 503 });
      }
      return Response.error();
    }
  })());
});
