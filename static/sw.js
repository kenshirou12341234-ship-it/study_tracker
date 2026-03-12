// キャッシュ名（バージョン管理用）
const CACHE_NAME = 'study-record-v1';

// キャッシュするファイルのリスト
const urlsToCache = [
  '/records/',
  '/static/manifest.json',
  '/static/goukaku-penguin-192.png',
  '/static/goukaku-penguin-512.png',
];

// Service Worker のインストール時の処理
self.addEventListener('install', (event) => {
  console.log('Service Worker: インストール中...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('Service Worker: キャッシュを開きました');
        return cache.addAll(urlsToCache);
      })
  );
});

// Service Worker の有効化時の処理
self.addEventListener('activate', (event) => {
  console.log('Service Worker: 有効化中...');
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log('Service Worker: 古いキャッシュを削除:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// ネットワークリクエストの処理
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        // キャッシュにあればキャッシュから返す
        if (response) {
          console.log('Service Worker: キャッシュから返します:', event.request.url);
          return response;
        }
        // キャッシュになければネットワークから取得
        console.log('Service Worker: ネットワークから取得:', event.request.url);
        return fetch(event.request);
      })
  );
});