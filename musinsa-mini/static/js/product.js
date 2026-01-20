import { fetchJSON, formatPriceKRW, isWished, toggleWish } from "./api.js";

function setStatus(msg) {
  const el = document.querySelector("#status");
  el.textContent = msg || "";
}

function escapeHtml(s) {
  return String(s)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function reviewCount(p) {
  return Array.isArray(p.reviews) ? p.reviews.length : 0;
}

export async function initProductPage(productId) {
  const root = document.querySelector("#productDetail");
  setStatus("로딩 중...");

  try {
    const p = await fetchJSON(`/api/products/${productId}`);
    const img = (p.images && p.images[0]) || p.thumbnail || "";

    const wished = isWished(productId);
    const rating = Number(p.rating || 0).toFixed(2);
    const rCount = reviewCount(p);

    root.innerHTML = `
      <img class="product-detail__img" src="${img}" alt="${escapeHtml(p.title)}" />
      <div class="product-detail__box">
        <h1 class="product-detail__title">${escapeHtml(p.title)}</h1>

        <div class="card__meta">
          <span>${escapeHtml(p.category || "")}</span>
          <strong>${formatPriceKRW(p.price)}</strong>
        </div>

        <div class="card__meta">
          <span>평점 ${rating}</span>
          <span>리뷰 ${rCount}</span>
        </div>

        <p class="product-detail__desc">${escapeHtml(p.description || "")}</p>

        <div class="qty">
          <label for="qtyInput">수량</label>
          <input id="qtyInput" type="number" min="1" value="1" />
          <button id="addBtn" class="btn">장바구니 담기</button>
          <button id="wishBtn" class="btn btn--ghost">${wished ? "♥ 찜됨" : "♡ 찜"}</button>
          <a class="btn btn--ghost" href="/cart">장바구니 보기</a>
        </div>
      </div>
    `;

    document.querySelector("#addBtn").addEventListener("click", async () => {
      const qty = Number(document.querySelector("#qtyInput").value || 1);
      try {
        await fetchJSON("/api/cart", {
          method: "POST",
          body: JSON.stringify({ productId, qty: Math.max(1, qty) }),
        });
        setStatus("장바구니에 담았습니다.");
      } catch (e) {
        setStatus(`실패: ${e.message}`);
      }
    });

    document.querySelector("#wishBtn").addEventListener("click", () => {
      const on = toggleWish(productId);
      document.querySelector("#wishBtn").textContent = on ? "♥ 찜됨" : "♡ 찜";
      setStatus(on ? "찜 목록에 추가했습니다." : "찜을 해제했습니다.");
    });

    setStatus("");
  } catch (e) {
    setStatus(`에러: ${e.message}`);
  }
}
