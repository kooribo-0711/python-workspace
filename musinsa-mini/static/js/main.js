import { fetchJSON, formatPriceKRW, getWishSet, toggleWish } from "./api.js";

const state = {
  q: "",
  category: "",
  limit: 24,
  skip: 0,

  // 정렬
  sortMode: "", // "", "price_asc", "reviews_desc"
  // UI/로딩
  total: 0,
  loading: false,
  onlyWish: false,

  // 무한스크롤: append 모드
  appendMode: true,
};

const els = {
  grid: document.querySelector("#productGrid"),
  status: document.querySelector("#status"),
  pager: document.querySelector("#pager"),

  searchInput: document.querySelector("#searchInput"),
  searchBtn: document.querySelector("#searchBtn"),
  categorySelect: document.querySelector("#categorySelect"),
  sortSelect: document.querySelector("#sortSelect"),
  onlyWish: document.querySelector("#onlyWish"),

  sentinel: document.querySelector("#sentinel"),
};

function setStatus(msg) {
  els.status.textContent = msg || "";
}

function escapeHtml(s) {
  return String(s)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

/* -----------------------------
 * 정렬 파라미터 계산
 * - price_asc: DummyJSON sortBy=price&order=asc :contentReference[oaicite:4]{index=4}
 * - reviews_desc: "리뷰 개수" 기준 내림차순 (클라이언트 정렬)
 *   (상품 스키마에 reviews 배열 존재 :contentReference[oaicite:5]{index=5})
 * ----------------------------- */
function getSortQuery() {
  if (state.sortMode === "price_asc") {
    return { sortBy: "price", order: "asc" };
  }
  // reviews_desc는 "리뷰 개수"로 정렬하므로 API 파라미터는 굳이 필요 없음
  return {};
}

function getPageInfo() {
  const page = Math.floor(state.skip / state.limit) + 1;
  const totalPages = Math.max(1, Math.ceil(state.total / state.limit) || 1);
  return { page, totalPages };
}

/* -----------------------------
 * 카드 렌더링
 * ----------------------------- */
function productCard(p, wishSet) {
  const thumb = p.thumbnail || (p.images && p.images[0]) || "";
  const wished = wishSet.has(String(p.id));

  const reviewCount = Array.isArray(p.reviews) ? p.reviews.length : 0;
  const rating = Number(p.rating || 0).toFixed(2);

  return `
    <article class="card" data-card="${p.id}">
      <div class="card__top">
        <a class="link" href="/product/${p.id}">
          <img class="card__img" src="${thumb}" alt="${escapeHtml(p.title)}" />
        </a>
        <button class="wish-btn ${wished ? "is-on" : ""}" data-wish="${p.id}" title="찜">
          ${wished ? "♥" : "♡"}
        </button>
      </div>

      <div class="card__body">
        <h3 class="card__title">
          <a class="link" href="/product/${p.id}">${escapeHtml(p.title)}</a>
        </h3>

        <div class="card__meta">
          <span>${escapeHtml(p.category || "")}</span>
          <strong>${formatPriceKRW(p.price)}</strong>
        </div>

        <div class="card__meta">
          <span>평점 ${rating}</span>
          <span>리뷰 ${reviewCount}</span>
        </div>

        <div class="card__actions">
          <button class="btn btn--ghost" data-add="${p.id}">장바구니</button>
          <a class="btn" href="/product/${p.id}">상세</a>
        </div>
      </div>
    </article>
  `;
}

function applyClientSideSort(products) {
  if (state.sortMode === "reviews_desc") {
    // 리뷰 개수 내림차순, 동률이면 rating 내림차순
    return [...products].sort((a, b) => {
      const ar = Array.isArray(a.reviews) ? a.reviews.length : 0;
      const br = Array.isArray(b.reviews) ? b.reviews.length : 0;
      if (br !== ar) return br - ar;
      return (Number(b.rating) || 0) - (Number(a.rating) || 0);
    });
  }
  return products;
}

function applyOnlyWishFilter(products) {
  if (!state.onlyWish) return products;
  const wishSet = getWishSet();
  return products.filter((p) => wishSet.has(String(p.id)));
}

/* -----------------------------
 * API 로드
 * ----------------------------- */
async function loadCategories() {
  try {
    const cats = await fetchJSON("/api/categories");
    const list = Array.isArray(cats) ? cats : (cats?.categories || []);

    for (const c of list) {
      const opt = document.createElement("option");
      opt.value = c.slug ?? c;
      opt.textContent = c.name ?? c;
      els.categorySelect.appendChild(opt);
    }
  } catch (e) {
    console.warn(e);
  }
}

async function fetchProductsPage() {
  const params = new URLSearchParams({
    limit: String(state.limit),
    skip: String(state.skip),
  });

  if (state.q) params.set("q", state.q);
  if (state.category) params.set("category", state.category);

  const sortQuery = getSortQuery();
  if (sortQuery.sortBy) params.set("sortBy", sortQuery.sortBy);
  if (sortQuery.order) params.set("order", sortQuery.order);

  return fetchJSON(`/api/products?${params.toString()}`);
}

/* -----------------------------
 * 페이지네이션 UI (세련된 pill + ... )
 * ----------------------------- */
function buildPageModel(page, totalPages) {
  // 현재 페이지 기준 앞뒤 2개씩, 처음/끝 고정 + ...
  const pages = new Set([1, totalPages, page - 2, page - 1, page, page + 1, page + 2]);
  const valid = [...pages].filter((p) => p >= 1 && p <= totalPages).sort((a, b) => a - b);

  const out = [];
  for (let i = 0; i < valid.length; i++) {
    const cur = valid[i];
    const prev = valid[i - 1];

    if (i > 0 && cur - prev > 1) out.push("dots");
    out.push(cur);
  }
  return out;
}

function renderPager() {
  const { page, totalPages } = getPageInfo();

  // 총 페이지가 1이면 깔끔하게 숨김
  if (totalPages <= 1) {
    els.pager.innerHTML = "";
    return;
  }

  const model = buildPageModel(page, totalPages);

  const prevDisabled = page <= 1;
  const nextDisabled = page >= totalPages;

  const parts = [];
  parts.push(`<button class="pager__btn" data-page="${page - 1}" ${prevDisabled ? "disabled" : ""}>‹</button>`);

  for (const item of model) {
    if (item === "dots") {
      parts.push(`<span class="pager__dots">…</span>`);
    } else {
      parts.push(`
        <button class="pager__btn ${item === page ? "is-active" : ""}"
                data-page="${item}">
          ${item}
        </button>
      `);
    }
  }

  parts.push(`<button class="pager__btn" data-page="${page + 1}" ${nextDisabled ? "disabled" : ""}>›</button>`);

  els.pager.innerHTML = parts.join("");
}

function scrollTopSmooth() {
  window.scrollTo({ top: 0, behavior: "smooth" });
}

/* -----------------------------
 * 렌더/로드 흐름
 * - resetAndLoad(): 새로운 조건(검색/카테고리/정렬/찜필터) 적용 시
 * - loadNextPageAppend(): 무한스크롤로 다음 페이지 추가
 * ----------------------------- */
function resetList() {
  state.skip = 0;
  state.total = 0;
  els.grid.innerHTML = "";
}

async function resetAndLoad() {
  if (state.loading) return;
  state.loading = true;

  resetList();
  setStatus("로딩 중...");

  try {
    const data = await fetchProductsPage();
    state.total = data.total ?? 0;

    // 1) page 데이터
    let products = data.products || [];
    // 2) "리뷰순" 등 클라이언트 정렬
    products = applyClientSideSort(products);
    // 3) 찜만 보기 필터
    products = applyOnlyWishFilter(products);

    const wishSet = getWishSet();
    els.grid.innerHTML = products.map((p) => productCard(p, wishSet)).join("");

    const shown = products.length;
    const { page, totalPages } = getPageInfo();
    setStatus(`페이지 ${page}/${totalPages} · 이번 페이지 ${shown}개 표시`);

    renderPager();
  } catch (e) {
    setStatus(`에러: ${e.message}`);
  } finally {
    state.loading = false;
  }
}

async function loadNextPageAppend() {
  if (state.loading) return;

  const { page, totalPages } = getPageInfo();
  if (page >= totalPages) return;

  state.loading = true;
  setStatus("다음 상품 불러오는 중...");

  try {
    state.skip += state.limit;

    const data = await fetchProductsPage();
    state.total = data.total ?? state.total;

    let products = data.products || [];
    products = applyClientSideSort(products);
    products = applyOnlyWishFilter(products);

    const wishSet = getWishSet();
    const html = products.map((p) => productCard(p, wishSet)).join("");
    els.grid.insertAdjacentHTML("beforeend", html);

    const nextPage = Math.floor(state.skip / state.limit) + 1;
    const totalPagesNow = Math.max(1, Math.ceil(state.total / state.limit) || 1);
    setStatus(`페이지 ${nextPage}/${totalPagesNow} · 누적 로드 중...`);

    renderPager();
  } catch (e) {
    // append 도중 실패하면 skip 되돌리는 게 안전
    state.skip = Math.max(0, state.skip - state.limit);
    setStatus(`에러: ${e.message}`);
  } finally {
    state.loading = false;
  }
}

/* -----------------------------
 * 장바구니/찜 이벤트
 * ----------------------------- */
async function addToCart(productId) {
  try {
    await fetchJSON("/api/cart", {
      method: "POST",
      body: JSON.stringify({ productId, qty: 1 }),
    });
    setStatus("장바구니에 담았습니다.");
  } catch (e) {
    setStatus(`장바구니 실패: ${e.message}`);
  }
}

function rerenderWishButtonsOnly() {
  // 찜 버튼 텍스트/상태만 빠르게 갱신
  const wishSet = getWishSet();
  document.querySelectorAll("[data-wish]").forEach((btn) => {
    const id = btn.dataset.wish;
    const on = wishSet.has(String(id));
    btn.classList.toggle("is-on", on);
    btn.textContent = on ? "♥" : "♡";
  });
}

/* -----------------------------
 * 무한스크롤 옵저버
 * ----------------------------- */
function setupInfiniteScroll() {
  const io = new IntersectionObserver(
    (entries) => {
      const first = entries[0];
      if (!first?.isIntersecting) return;
      // 무한스크롤은 appendMode일 때만
      if (!state.appendMode) return;
      loadNextPageAppend();
    },
    { root: null, rootMargin: "800px 0px", threshold: 0 }
  );

  io.observe(els.sentinel);
}

/* -----------------------------
 * 바인딩
 * ----------------------------- */
function bindEvents() {
  els.searchBtn.addEventListener("click", () => {
    state.q = els.searchInput.value.trim();
    state.appendMode = true; // 검색 후에도 무한스크롤 유지
    resetAndLoad();
  });

  els.searchInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") els.searchBtn.click();
  });

  els.categorySelect.addEventListener("change", () => {
    state.category = els.categorySelect.value;
    state.appendMode = true;
    resetAndLoad();
  });

  els.sortSelect.addEventListener("change", () => {
    state.sortMode = els.sortSelect.value; // "", "price_asc", "reviews_desc"
    state.appendMode = true;
    resetAndLoad();
  });

  els.onlyWish.addEventListener("change", () => {
    state.onlyWish = els.onlyWish.checked;

    // “찜만 보기”는 무한스크롤 UX가 애매해져서(찜은 개수가 적을 수 있음)
    // 페이지 단위로만 동작하도록 appendMode는 유지하되,
    // 초기 로드가 중요하니 그냥 resetAndLoad를 강제합니다.
    resetAndLoad();
  });

  // 카드 영역 이벤트 (장바구니/찜)
  els.grid.addEventListener("click", async (e) => {
    const addBtn = e.target.closest("[data-add]");
    if (addBtn) {
      const productId = Number(addBtn.dataset.add);
      if (Number.isFinite(productId)) addToCart(productId);
      return;
    }

    const wishBtn = e.target.closest("[data-wish]");
    if (wishBtn) {
      const productId = Number(wishBtn.dataset.wish);
      if (!Number.isFinite(productId)) return;

      toggleWish(productId);
      rerenderWishButtonsOnly();

      // 찜만 보기 상태에서는, 찜 해제 시 목록에서 사라져야 함
      if (state.onlyWish) resetAndLoad();
      return;
    }
  });

  // 페이지네이션 클릭
  els.pager.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-page]");
    if (!btn || btn.disabled) return;

    const targetPage = Number(btn.dataset.page);
    const { totalPages } = getPageInfo();
    if (!Number.isFinite(targetPage)) return;
    if (targetPage < 1 || targetPage > totalPages) return;

    // 페이지 클릭은 “해당 페이지로 점프(교체)”가 자연스러움
    state.appendMode = false;
    state.skip = (targetPage - 1) * state.limit;
    resetAndLoad();
    scrollTopSmooth();

    // 점프 후 다시 무한스크롤을 원하면 여기서 true로 바꿔도 되지만,
    // UX상 점프 이후는 사용자가 스크롤로 이어서 보게 하려면 true가 더 자연스러울 수 있음.
    // 초보자용으로는 동작이 헷갈리지 않게: 점프 후 다시 true로 되돌림
    state.appendMode = true;
  });
}

/* -----------------------------
 * Init
 * ----------------------------- */
(async function init() {
  bindEvents();
  setupInfiniteScroll();
  await loadCategories();
  await resetAndLoad();
})();
// DummyJSON 카테고리 중 패션에 해당하는 것만 사용 (필요하면 추가/삭제)
const FASHION_CATEGORIES = new Set([
  "mens-shirts",
  "mens-shoes",
  "mens-watches",
  "womens-dresses",
  "womens-shoes",
  "womens-watches",
  "womens-bags",
  "tops",
  "sunglasses",
]);
