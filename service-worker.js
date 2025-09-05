self.addEventListener("install", event => {
  event.waitUntil(
    caches.open("cache-jeu").then(cache => {
      return cache.addAll([
        "/",
        "/index.html",
        "/main.py",
        "/manifest.json",
        "/images/icon.png"
      ]);
    })
  );
});

self.addEventListener("fetch", event => {
  event.respondWith(
    caches.match(event.request).then(resp => resp || fetch(event.request))
  );
});