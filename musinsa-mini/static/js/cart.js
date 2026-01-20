import { fetchJSON, formatPriceKRW } from "./api.js";

const root = document.querySelector("#cartRoot");

function setStatus(msg) {
  document.querySelector("#status").textContent = msg || "";
}

function escapeHtml(s) {
  return String(s)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function cartItemRow(item) {
  const p = item.product;
  const img = p.thumbnail || (p.images && p.images[0]) || "";
  return `
    <div class="cart-item" data-id="${p.id}">
      <img class="cart-item__img" src="${img}" alt="${escapeHtml(p.title)}" />
      <div>
        <p class="cart-item__title">${escapeHtml(p.title)}</p>
        <div class="cart-item__meta">
          <span>${escapeHtml(p.category || "")}</span>
          · <strong>${formatPriceKRW(p.price)}</strong>
        </div>
      </div>
      <div class="qty">
        <input class="qty-input" type="number" min="0" value="${item.qty}" />
        <button class="btn btn--ghost btn-remove">삭제</button>
      </div>
    </div>
  `;
}

async function loadCart() {
  setStatus("로딩 중...");
  try {
    const data = await fetchJSON("/api/cart");
    const items = data.items || [];

    if (items.length === 0) {
      root.innerHTML = `
        <p class="status">장바구니가 비어 있습니다. <a class="link" href="/">상품 보러가기</a></p>
      `;
      setStatus("");
      return;
    }

    root.innerHTML = `
      ${items.map(cartItemRow).join("")}
      <div class="cart-summary">
        <span>총 수량: ${data.totalQty}</span>
        <span>합계: ${formatPriceKRW(data.totalPrice)}</span>
      </div>
    `;

    setStatus("");

  } catch (e) {
    setStatus(`에러: ${e.message}`);
  }
}

async function updateQty(productId, qty) {
  await fetchJSON("/api/cart", {
    method: "PATCH",
    body: JSON.stringify({ productId, qty }),
  });
}

async function removeItem(productId) {
  await fetchJSON("/api/cart", {
    method: "DELETE",
    body: JSON.stringify({ productId }),
  });
}

root.addEventListener("change", async (e) => {
  const input = e.target.closest(".qty-input");
  if (!input) return;

  const row = e.target.closest("[data-id]");
  const productId = Number(row.dataset.id);
  const qty = Number(input.value);

  try {
    await updateQty(productId, Number.isFinite(qty) ? qty : 1);
    await loadCart();
  } catch (err) {
    setStatus(`수정 실패: ${err.message}`);
  }
});

root.addEventListener("click", async (e) => {
  const btn = e.target.closest(".btn-remove");
  if (!btn) return;

  const row = e.target.closest("[data-id]");
  const productId = Number(row.dataset.id);

  try {
    await removeItem(productId);
    await loadCart();
  } catch (err) {
    setStatus(`삭제 실패: ${err.message}`);
  }
});

loadCart();
