export async function fetchJSON(url, options = {}) {
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  const data = await res.json().catch(() => ({}));

  if (!res.ok) {
    const message = data?.message || `Request failed (${res.status})`;
    throw new Error(message);
  }
  return data;
}

export function formatPriceKRW(value) {
  const n = Number(value) || 0;
  return n.toLocaleString("ko-KR") + " 원";
}

/* -----------------------------
 * 찜(위시리스트) - LocalStorage
 * ----------------------------- */
const WISH_KEY = "mini_musinsa_wishlist_v1";

export function getWishSet() {
  try {
    const raw = localStorage.getItem(WISH_KEY);
    const arr = raw ? JSON.parse(raw) : [];
    return new Set(arr.map(String));
  } catch {
    return new Set();
  }
}

export function saveWishSet(set) {
  const arr = Array.from(set);
  localStorage.setItem(WISH_KEY, JSON.stringify(arr));
}

export function isWished(productId) {
  const set = getWishSet();
  return set.has(String(productId));
}

export function toggleWish(productId) {
  const set = getWishSet();
  const key = String(productId);

  if (set.has(key)) set.delete(key);
  else set.add(key);

  saveWishSet(set);
  return set.has(key); // 토글 후 상태
}
