import pytest
from unittest.mock import patch, MagicMock
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        client.environ_base["HTTP_AUTHORIZATION"] = "Bearer campus-eats-token"
        yield client


@pytest.fixture(autouse=True)
def reset_store():
    """Reset the store and idempotency store before each test."""
    from app import store, idempotency_store, rate_limits
    store.orders.clear()
    store.carts.clear()
    store.next_order_id = 1
    idempotency_store.clear()
    rate_limits.clear()


# --- Cart tests ---

def test_add_cart_item_success(client):
    resp = client.post("/carts/items", json={
        "studentId": 17,
        "itemId": 101,
        "quantity": 2
    })
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["studentId"] == 17
    assert len(data["items"]) == 1
    assert data["items"][0]["itemId"] == 101


def test_add_cart_item_invalid_body(client):
    resp = client.post("/carts/items", json={
        "studentId": "abc",
        "itemId": 101,
        "quantity": 2
    })
    assert resp.status_code == 400


# --- Order creation tests ---

@patch("app.call_payment_service", return_value="success")
def test_create_order_success(mock_pay, client):
    resp = client.post("/orders", json={
        "studentId": 17,
        "items": [{"itemId": 101, "quantity": 2}]
    }, headers={"Idempotency-Key": "key-001"})

    assert resp.status_code == 201
    data = resp.get_json()
    assert data["studentId"] == 17
    assert data["status"] == "placed"
    assert "Location" in resp.headers
    assert resp.headers["Location"] == f"/orders/{data['id']}"


@patch("app.call_payment_service", return_value="success")
def test_idempotent_repeat(mock_pay, client):
    body = {
        "studentId": 17,
        "items": [{"itemId": 101, "quantity": 2}]
    }
    headers = {"Idempotency-Key": "key-002"}

    resp1 = client.post("/orders", json=body, headers=headers)
    resp2 = client.post("/orders", json=body, headers=headers)

    assert resp1.status_code == 201
    assert resp2.status_code == 201

    # Same order returned, no duplicate created
    assert resp1.get_json()["id"] == resp2.get_json()["id"]

    # Payment should only be called once
    assert mock_pay.call_count == 1


def test_create_order_missing_idempotency_key(client):
    resp = client.post("/orders", json={
        "studentId": 17,
        "items": [{"itemId": 101, "quantity": 2}]
    })
    assert resp.status_code == 400
    assert "Idempotency-Key" in resp.get_json()["detail"]


def test_create_order_invalid_body(client):
    resp = client.post("/orders", json={
        "studentId": -1,
        "items": [{"itemId": 101, "quantity": 2}]
    }, headers={"Idempotency-Key": "key-003"})
    assert resp.status_code == 400


@patch("app.call_payment_service", return_value="refused")
def test_payment_refused_returns_422(mock_pay, client):
    resp = client.post("/orders", json={
        "studentId": 17,
        "items": [{"itemId": 101, "quantity": 2}]
    }, headers={"Idempotency-Key": "key-004"})

    assert resp.status_code == 422
    data = resp.get_json()
    assert data["title"] == "Payment refused"


@patch("app.call_payment_service", return_value="unavailable")
def test_payment_unavailable_returns_503(mock_pay, client):
    resp = client.post("/orders", json={
        "studentId": 17,
        "items": [{"itemId": 101, "quantity": 2}]
    }, headers={"Idempotency-Key": "key-005"})

    assert resp.status_code == 503
    data = resp.get_json()
    assert data["title"] == "Payment service unavailable"


# --- Get order tests ---

@patch("app.call_payment_service", return_value="success")
def test_get_order_success(mock_pay, client):
    create_resp = client.post("/orders", json={
        "studentId": 17,
        "items": [{"itemId": 101, "quantity": 2}]
    }, headers={"Idempotency-Key": "key-006"})

    order_id = create_resp.get_json()["id"]
    resp = client.get(f"/orders/{order_id}")
    assert resp.status_code == 200
    assert resp.get_json()["id"] == order_id


def test_get_order_unknown_returns_404(client):
    resp = client.get("/orders/999")
    assert resp.status_code == 404
    data = resp.get_json()
    assert data["status"] == 404


@patch("app.call_payment_service", return_value="success")
def test_conditional_get_and_stale_update(mock_pay, client):
    created = client.post("/orders", json={
        "studentId": 17, "items": [{"itemId": 101, "quantity": 1}]
    }, headers={"Idempotency-Key": "key-etag"})
    order_id = created.get_json()["id"]
    read = client.get(f"/orders/{order_id}")
    etag = read.headers["ETag"]

    assert client.get(f"/orders/{order_id}", headers={"If-None-Match": etag}).status_code == 304
    stale = client.put(f"/orders/{order_id}", json={
        "studentId": 17, "items": [{"itemId": 101, "quantity": 3}]
    }, headers={"If-Match": '"stale"'})
    assert stale.status_code == 412


def test_missing_authorization_returns_401(client):
    response = client.get("/orders/1", headers={"Authorization": ""})
    assert response.status_code == 401


def test_options_and_not_acceptable(client):
    options = client.open("/orders", method="OPTIONS")
    assert options.status_code == 204
    assert options.headers["Allow"] == "GET, POST, OPTIONS"
    assert options.headers["Access-Control-Allow-Origin"] == "https://campuseats.example"
    assert client.get("/orders/1", headers={"Accept": "text/html"}).status_code == 406


# --- List orders tests ---

@patch("app.call_payment_service", return_value="success")
def test_list_orders_success(mock_pay, client):
    client.post("/orders", json={
        "studentId": 17,
        "items": [{"itemId": 101, "quantity": 1}]
    }, headers={"Idempotency-Key": "key-007"})

    resp = client.get("/orders?studentId=17")
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) == 1
    assert data[0]["studentId"] == 17


def test_list_orders_missing_student_id(client):
    resp = client.get("/orders")
    assert resp.status_code == 400


def test_list_orders_invalid_student_id(client):
    resp = client.get("/orders?studentId=abc")
    assert resp.status_code == 400


# --- Cancel order tests ---

@patch("app.call_payment_service", return_value="success")
def test_cancel_order_success(mock_pay, client):
    create_resp = client.post("/orders", json={
        "studentId": 17,
        "items": [{"itemId": 101, "quantity": 1}]
    }, headers={"Idempotency-Key": "key-008"})

    order_id = create_resp.get_json()["id"]
    resp = client.post(f"/orders/{order_id}/cancellation")
    assert resp.status_code == 202
    assert resp.get_json()["status"] == "cancelled"


@patch("app.call_payment_service", return_value="success")
def test_cancel_already_cancelled_returns_409(mock_pay, client):
    create_resp = client.post("/orders", json={
        "studentId": 17,
        "items": [{"itemId": 101, "quantity": 1}]
    }, headers={"Idempotency-Key": "key-009"})

    order_id = create_resp.get_json()["id"]
    client.post(f"/orders/{order_id}/cancellation")

    resp = client.post(f"/orders/{order_id}/cancellation")
    assert resp.status_code == 409


def test_cancel_unknown_order_returns_404(client):
    resp = client.post("/orders/999/cancellation")
    assert resp.status_code == 404
