self.addEventListener('install', (e) => {
  self.skipWaiting(); // Force active activation
  e.waitUntil(
    caches.open('plant-app-v2').then((cache) => {
      return cache.addAll(['/', '/manifest.json']);
    })
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== 'plant-app-v2') {
            return caches.delete(key);
          }
        })
      );
    })
  );
});

self.addEventListener('fetch', (e) => {
  e.respondWith(
    fetch(e.request).catch(() => caches.match(e.request))
  );
});