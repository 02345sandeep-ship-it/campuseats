import os
import time
import random
import hashlib
import json
import requests
from flask import Flask, jsonify, request, make_response

from models import OrderItem
from store import Store
from errors import problem


app = Flask(__name__)
store = Store()

PAYMENTS_URL = os.getenv("PAYMENTS_URL", "http://localhost:8082")

idempotency_store = {}
rate_limits = {}

AUTH_TOKEN = os.getenv("API_TOKEN", "campus-eats-token")
RATE_LIMIT = 100
RATE_WINDOW_SECONDS = 60


def order_etag(order):
    """Produce a strong ETag from the current representation."""
    encoded = json.dumps(order.to_dict(), sort_keys=True, separators=(",", ":"))
    return '"' + hashlib.sha256(encoded.encode("utf-8")).hexdigest() + '"'


def allowed_methods(path):
    if path == "/orders":
        return "GET, POST, OPTIONS"
    if path.startswith("/orders/") and path.endswith("/cancellation"):
        return "POST, OPTIONS"
    if path.startswith("/orders/"):
        return "GET, PUT, OPTIONS"
    if path == "/carts/items":
        return "POST, OPTIONS"
    return "GET, OPTIONS"


@app.before_request
def enforce_http_contract():
    """Apply shared HTTP policy before a resource handler runs."""
    if request.method == "OPTIONS":
        response = make_response("", 204)
        response.headers["Allow"] = allowed_methods(request.path)
        return response

    # Health checks are intentionally public; the business API is protected.
    if request.path != "/health":
        if request.headers.get("Authorization") != f"Bearer {AUTH_TOKEN}":
            return problem(401, "Unauthorized", "Use Authorization: Bearer <token>.")

    accept = request.headers.get("Accept", "*/*")
    if request.path != "/health" and "*/*" not in accept and "application/json" not in accept:
        return problem(406, "Not Acceptable", "This API only produces application/json.")

    client = request.headers.get("Authorization", request.remote_addr)
    now = time.time()
    window_start, count = rate_limits.get(client, (now, 0))
    if now - window_start >= RATE_WINDOW_SECONDS:
        window_start, count = now, 0
    if count >= RATE_LIMIT:
        response, status = problem(429, "Too Many Requests", "Rate limit exceeded.")
        response.headers["Retry-After"] = str(RATE_WINDOW_SECONDS)
        return response, status
    rate_limits[client] = (window_start, count + 1)


@app.after_request
def add_response_headers(response):
    """Headers sent on every response, including errors and preflights."""
    response.headers["Access-Control-Allow-Origin"] = "https://campuseats.example"
    response.headers["Access-Control-Allow-Methods"] = allowed_methods(request.path)
    response.headers["Access-Control-Allow-Headers"] = (
        "Authorization, Content-Type, Accept, Idempotency-Key, If-Match, If-None-Match, X-HTTP-Method-Override"
    )
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-RateLimit-Limit"] = str(RATE_LIMIT)
    client = request.headers.get("Authorization", request.remote_addr)
    count = rate_limits.get(client, (0, 0))[1]
    response.headers["X-RateLimit-Remaining"] = str(max(0, RATE_LIMIT - count))
    return response


def validate_order(data):
    if not isinstance(data, dict):
        return "Request body must be a JSON object."

    if not isinstance(data.get("studentId"), int):
        return "studentId must be an integer."

    if data["studentId"] <= 0:
        return "studentId must be greater than 0."

    if not isinstance(data.get("items"), list) or len(data["items"]) == 0:
        return "items must be a non-empty array."

    for item in data["items"]:
        if not isinstance(item, dict):
            return "Each item must be an object."

        if not isinstance(item.get("itemId"), int):
            return "itemId must be an integer."

        if item["itemId"] <= 0:
            return "itemId must be greater than 0."

        if not isinstance(item.get("quantity"), int):
            return "quantity must be an integer."

        if item["quantity"] <= 0:
            return "quantity must be greater than 0."

    return None


def validate_cart(data):
    if not isinstance(data, dict):
        return "Request body must be a JSON object."

    for field in ["studentId", "itemId", "quantity"]:
        if not isinstance(data.get(field), int):
            return field + " must be an integer."

    if data["studentId"] <= 0:
        return "studentId must be greater than 0."

    if data["itemId"] <= 0:
        return "itemId must be greater than 0."

    if data["quantity"] <= 0:
        return "quantity must be greater than 0."

    return None


def call_payment_service(key, student_id):
    payment_data = {
        "studentId": student_id,
        "amount": 100
    }

    headers = {
        "Idempotency-Key": key
    }

    max_attempts = 3

    for attempt in range(max_attempts):
        try:
            response = requests.post(
                f"{PAYMENTS_URL}/charges",
                json=payment_data,
                headers=headers,
                timeout=2
            )

            if response.status_code >= 500:
                if attempt < max_attempts - 1:
                    delay = (0.2 * (2 ** attempt)) + random.uniform(0, 0.1)
                    time.sleep(delay)
                    continue

                return "unavailable"

            if response.status_code >= 400:
                return "refused"

            return "success"

        except requests.RequestException:
            if attempt < max_attempts - 1:
                delay = (0.2 * (2 ** attempt)) + random.uniform(0, 0.1)
                time.sleep(delay)
                continue

            return "unavailable"

    return "unavailable"


@app.post("/orders")
def create_order():
    key = request.headers.get("Idempotency-Key")

    if not key:
        return problem(
            400,
            "Missing Idempotency-Key",
            "Idempotency-Key header is required."
        )

    if key in idempotency_store:
        saved = idempotency_store[key]

        response = jsonify(saved["body"])
        response.status_code = saved["status"]

        if "location" in saved:
            response.headers["Location"] = saved["location"]

        return response

    data = request.get_json(silent=True)

    error = validate_order(data)

    if error:
        return problem(400, "Invalid request", error)

    items = [
        OrderItem(
            item_id=item["itemId"],
            quantity=item["quantity"]
        )
        for item in data["items"]
    ]

    payment_result = call_payment_service(
        key,
        data["studentId"]
    )

    if payment_result == "unavailable":
        return problem(
            503,
            "Payment service unavailable",
            "The payment service could not be reached.",
            "/errors/payment-service-unavailable"
        )

    if payment_result == "refused":
        return problem(
            422,
            "Payment refused",
            "The payment service refused the payment.",
            "/errors/payment-refused"
        )

    order = store.create_order(
        data["studentId"],
        items
    )

    body = order.to_dict()
    location = f"/orders/{order.id}"

    idempotency_store[key] = {
        "body": body,
        "status": 201,
        "location": location
    }

    result = jsonify(body)
    result.status_code = 201
    result.headers["Location"] = location

    return result


@app.get("/orders/<int:order_id>")
def get_order(order_id):
    order = store.get_order(order_id)

    if order is None:
        return problem(
            404,
            "Order not found",
            f"No order exists with id {order_id}."
        )

    etag = order_etag(order)
    if request.headers.get("If-None-Match") == etag:
        response = make_response("", 304)
        response.headers["ETag"] = etag
        response.headers["Cache-Control"] = "public, max-age=60"
        return response

    response = jsonify(order.to_dict())
    response.headers["ETag"] = etag
    response.headers["Cache-Control"] = "public, max-age=60"
    return response, 200


@app.put("/orders/<int:order_id>")
def replace_order(order_id):
    order = store.get_order(order_id)
    if order is None:
        return problem(404, "Order not found", f"No order exists with id {order_id}.")

    current_etag = order_etag(order)
    supplied_etag = request.headers.get("If-Match")
    if not supplied_etag:
        return problem(428, "Precondition Required", "If-Match header is required for an update.")
    if supplied_etag != current_etag:
        return problem(412, "Precondition Failed", "The order changed; fetch its current ETag before retrying.")

    data = request.get_json(silent=True)
    error = validate_order(data)
    if error:
        return problem(400, "Invalid request", error)

    items = [OrderItem(item_id=item["itemId"], quantity=item["quantity"]) for item in data["items"]]
    order = store.replace_order(order_id, data["studentId"], items)
    response = jsonify(order.to_dict())
    response.headers["ETag"] = order_etag(order)
    response.headers["Cache-Control"] = "no-store"
    return response, 200


@app.get("/orders")
def list_orders():
    student_id = request.args.get("studentId")

    if student_id is None:
        return problem(
            400,
            "Invalid query",
            "studentId is required."
        )

    try:
        student_id = int(student_id)
    except ValueError:
        return problem(
            400,
            "Invalid query",
            "studentId must be an integer."
        )

    if student_id <= 0:
        return problem(
            400,
            "Invalid query",
            "studentId must be greater than 0."
        )

    orders = store.list_orders(student_id)

    return jsonify([
        order.to_dict() for order in orders
    ]), 200


@app.post("/orders/<int:order_id>/cancellation")
def cancel_order(order_id):
    order = store.get_order(order_id)

    if order is None:
        return problem(
            404,
            "Order not found",
            f"No order exists with id {order_id}."
        )

    if order.status == "cancelled":
        return problem(
            409,
            "Order already cancelled",
            "The order has already been cancelled."
        )

    order = store.cancel_order(order_id)

    return jsonify(order.to_dict()), 202


@app.post("/carts/items")
def add_cart_item():
    data = request.get_json(silent=True)

    error = validate_cart(data)

    if error:
        return problem(400, "Invalid request", error)

    cart = store.add_cart_item(
        data["studentId"],
        data["itemId"],
        data["quantity"]
    )

    return jsonify(cart.to_dict()), 201


@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8081"))
    )
