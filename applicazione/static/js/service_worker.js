self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open('my-cache').then(function(cache) {
            return cache.addAll([
                '/',
                '/static/icons/android-chrome-36x36.png',
                '/static/icons/android-chrome-72x72.png',
                '/static/icons/android-chrome-192x192.png',
                '/static/icons/android-chrome-512x512.png',
                '/static/site.webmanifest'
            ]);
        })
    );
});

self.addEventListener('fetch', function(event) {
    event.respondWith(
        caches.match(event.request).then(function(response) {
            return response || fetch(event.request);
        })
    );
});