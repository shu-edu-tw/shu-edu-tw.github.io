// Service Worker for Caching
// ==========================

const CACHE_NAME = 'shu-website-v3';
const urlsToCache = [
    '/',
    '/index.html',
    '/css/style.css',
    '/js/main.js',
    '/js/performance.js',
    '/images/shu-logo.webp',
    '/images/Banner.webp',
    '/pages/about.html',
    '/pages/academics.html',
    '/pages/admissions.html',
    '/pages/alumni.html',
    '/pages/campus-life.html',
    '/pages/contact.html',
    '/pages/courses.html',
    '/pages/faculty.html',
    '/pages/news.html',
    '/news/2024-10-04-marshall-president-visit.html',
    '/news/2024-10-08-printing-gold-award.html',
    '/news/2024-10-11-golden-harvest-award.html',
    '/news/2024-10-18-campus-recruitment.html'
];

// Install event
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('Opened cache');
                return cache.addAll(urlsToCache);
            })
            .catch(err => {
                console.error('Cache installation failed:', err);
            })
    );
    self.skipWaiting();
});

// Fetch event with network-first strategy for HTML
self.addEventListener('fetch', event => {
    const { request } = event;
    const url = new URL(request.url);
    
    // Network-first for HTML pages
    if (request.headers.get('accept').includes('text/html')) {
        event.respondWith(
            fetch(request)
                .then(response => {
                    const responseClone = response.clone();
                    caches.open(CACHE_NAME).then(cache => {
                        cache.put(request, responseClone);
                    });
                    return response;
                })
                .catch(() => {
                    return caches.match(request);
                })
        );
        return;
    }
    
    // Cache-first for other resources
    event.respondWith(
        caches.match(request)
            .then(response => {
                if (response) {
                    return response;
                }
                return fetch(request).then(response => {
                    // Only cache valid responses
                    if (!response || response.status !== 200 || response.type === 'error') {
                        return response;
                    }
                    const responseClone = response.clone();
                    caches.open(CACHE_NAME).then(cache => {
                        cache.put(request, responseClone);
                    });
                    return response;
                });
            })
    );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    return self.clients.claim();
});

