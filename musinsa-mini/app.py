from __future__ import annotations

import os
from typing import Any, Dict, Tuple

import requests
from flask import Flask, jsonify, render_template, request, session
from dotenv import load_dotenv

load_dotenv()

DUMMYJSON_BASE_URL = "https://dummyjson.com"
# DummyJSON은 제품/검색 등 더미 데이터를 무료로 제공하는 API입니다. :contentReference[oaicite:1]{index=1}

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key-change-me")


# -----------------------------
# 유틸: 세션 장바구니
# cart 구조: { "<product_id>": {"qty": int, "product": {...}} }
# -----------------------------
def get_cart() -> Dict[str, Any]:
    cart = session.get("cart")
    if not isinstance(cart, dict):
        cart = {}
        session["cart"] = cart
    return cart


def save_cart(cart: Dict[str, Any]) -> None:
    session["cart"] = cart
    session.modified = True


# -----------------------------
# 유틸: DummyJSON 호출
# -----------------------------
def dummyjson_get(path: str, params: Dict[str, Any] | None = None) -> Tuple[Dict[str, Any], int]:
    """
    DummyJSON로 GET 요청을 보내고 (json, status_code)를 반환합니다.
    """
    url = f"{DUMMYJSON_BASE_URL}{path}"
    try:
        r = requests.get(url, params=params, timeout=8)
        data = r.json() if r.headers.get("Content-Type", "").startswith("application/json") else {}
        return data, r.status_code
    except requests.RequestException:
        return {"message": "Upstream API request failed."}, 502


# -----------------------------
# 페이지 라우트
# -----------------------------
@app.get("/")
def page_index():
    return render_template("index.html")


@app.get("/product/<int:product_id>")
def page_product(product_id: int):
    return render_template("product.html", product_id=product_id)


@app.get("/cart")
def page_cart():
    return render_template("cart.html")


# -----------------------------
# 프론트에서 쓰는 API 라우트 (프록시)
# -----------------------------
@app.get("/api/products")
def api_products():
    """
    쿼리:
      - q: 검색어
      - category: 카테고리
      - limit, skip: 페이지네이션
      - sortBy: 정렬 기준 (예: price, rating, title ...)
      - order: asc / desc
    """
    q = (request.args.get("q") or "").strip()
    category = (request.args.get("category") or "").strip()

    limit = request.args.get("limit", "24")
    skip = request.args.get("skip", "0")

    sort_by = (request.args.get("sortBy") or "").strip()
    order = (request.args.get("order") or "").strip()

    params = {"limit": limit, "skip": skip}

    # DummyJSON Sort: sortBy + order :contentReference[oaicite:3]{index=3}
    if sort_by:
        params["sortBy"] = sort_by
    if order:
        params["order"] = order

    if category:
        data, status = dummyjson_get(f"/products/category/{category}", params=params)
    elif q:
        data, status = dummyjson_get("/products/search", params={**params, "q": q})
    else:
        data, status = dummyjson_get("/products", params=params)

    return jsonify(data), status



@app.get("/api/products/<int:product_id>")
def api_product_detail(product_id: int):
    data, status = dummyjson_get(f"/products/{product_id}")
    return jsonify(data), status


@app.get("/api/categories")
def api_categories():
    data, status = dummyjson_get("/products/categories")
    return jsonify(data), status


# -----------------------------
# 장바구니 API
# -----------------------------
@app.get("/api/cart")
def api_cart_get():
    cart = get_cart()
    items = list(cart.values())
    total_qty = sum(int(i["qty"]) for i in items)
    total_price = sum(float(i["qty"]) * float(i["product"].get("price", 0)) for i in items)
    return jsonify({"items": items, "totalQty": total_qty, "totalPrice": total_price})


@app.post("/api/cart")
def api_cart_add():
    """
    body: { "productId": number, "qty": number }
    """
    body = request.get_json(silent=True) or {}
    product_id = body.get("productId")
    qty = int(body.get("qty", 1))

    if not isinstance(product_id, int) or qty <= 0:
        return jsonify({"message": "Invalid payload."}), 400

    product, status = dummyjson_get(f"/products/{product_id}")
    if status != 200:
        return jsonify({"message": "Product not found."}), 404

    cart = get_cart()
    key = str(product_id)

    if key in cart:
        cart[key]["qty"] = int(cart[key]["qty"]) + qty
    else:
        cart[key] = {"qty": qty, "product": product}

    save_cart(cart)
    return jsonify({"message": "Added to cart."}), 201


@app.patch("/api/cart")
def api_cart_update_qty():
    """
    body: { "productId": number, "qty": number }  # qty를 새 값으로 설정
    """
    body = request.get_json(silent=True) or {}
    product_id = body.get("productId")
    qty = body.get("qty")

    if not isinstance(product_id, int) or not isinstance(qty, int):
        return jsonify({"message": "Invalid payload."}), 400

    cart = get_cart()
    key = str(product_id)

    if key not in cart:
        return jsonify({"message": "Item not in cart."}), 404

    if qty <= 0:
        del cart[key]
    else:
        cart[key]["qty"] = qty

    save_cart(cart)
    return jsonify({"message": "Cart updated."})


@app.delete("/api/cart")
def api_cart_remove():
    """
    body: { "productId": number }
    """
    body = request.get_json(silent=True) or {}
    product_id = body.get("productId")
    if not isinstance(product_id, int):
        return jsonify({"message": "Invalid payload."}), 400

    cart = get_cart()
    key = str(product_id)
    if key in cart:
        del cart[key]
        save_cart(cart)

    return jsonify({"message": "Removed."})


if __name__ == "__main__":
    app.run(debug=True)
