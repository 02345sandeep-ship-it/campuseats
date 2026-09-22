# CS543 Web Services — Assignment 5: HTTP Methods & Headers

**Team ID:** CampusEats-A5

| Name | Roll no. |
| --- | --- |
| Sandeep Gupta | 20252651045 |
| Deepankar Bej | 20252651018 |
| Rikam Gouda | 20252651040 |
| Shivam Rajput | 20252651052 |

The executable service is in [`services/orders`](../../services/orders). Its OpenAPI contract is
[`openapi.yaml`](../../services/orders/openapi.yaml), and its automated tests are in
[`test_app.py`](../../services/orders/test_app.py).

## CampusEats method map

| Resource | Method | Purpose | Safe | Idempotent | Success |
| --- | --- | --- | --- | --- | --- |
| `/orders?studentId=17` | GET | List one student's orders | Yes | Yes | 200 |
| `/orders` | POST | Create an order | No | No* | 201 + `Location` |
| `/orders/1` | GET | Read one order | Yes | Yes | 200 + `ETag` |
| `/orders/1` | PUT | Replace an order representation | No | Yes | 200 + `ETag` |
| `/orders/1/cancellation` | POST | Create the order's cancellation sub-resource | No | No | 202 |
| `/carts/items` | POST | Add an item to a cart | No | No | 201 |
| any listed resource | OPTIONS | Discover supported methods / answer preflight | Yes | Yes | 204 + `Allow` |

`POST /orders` is made retry-safe with `Idempotency-Key`: a repeat with the same key returns the
original 201 representation and does not charge or create a second order. The cancellation action
is a noun sub-resource, not an action URL such as `/cancelOrder`.

## Headers table

| Endpoint | Important request headers | Important response headers |
| --- | --- | --- |
| `POST /orders` | `Authorization`, `Content-Type`, `Accept`, `Idempotency-Key` | `Content-Type`, `Location`, rate-limit, CORS, security headers |
| `GET /orders/{id}` | `Authorization`, `Accept`, optional `If-None-Match` | `Content-Type`, `ETag`, `Cache-Control`, rate-limit, CORS, security headers |
| `PUT /orders/{id}` | `Authorization`, `Content-Type`, `Accept`, `If-Match` | `Content-Type`, new `ETag`, `Cache-Control: no-store`, rate-limit, CORS, security headers |
| `POST /orders/{id}/cancellation` | `Authorization`, `Accept` | `Content-Type`, rate-limit, CORS, security headers |
| `POST /carts/items` | `Authorization`, `Content-Type`, `Accept` | `Content-Type`, rate-limit, CORS, security headers |
| `OPTIONS` | `Origin`, `Access-Control-Request-Method` | `Allow`, `Access-Control-Allow-Origin`, `Access-Control-Allow-Methods`, `Access-Control-Allow-Headers` |

Every JSON body uses `Content-Type: application/json`. If `Accept` excludes JSON, the service returns
`406 Not Acceptable`. All protected resources require `Authorization: Bearer campus-eats-token` in
this demonstration. The service also sends `X-Content-Type-Options: nosniff`, HSTS, and per-client
`X-RateLimit-Limit` / `X-RateLimit-Remaining`; a client over its budget receives `429` and
`Retry-After`.

## Safe-retry plan

| Risky endpoint | Mechanism | Why |
| --- | --- | --- |
| `POST /orders` | `Idempotency-Key` | A retry could otherwise create two orders and charge twice. |
| `PUT /orders/{id}` | `If-Match` | Rejects a stale editor with 412 instead of overwriting a newer representation. |
| `GET /orders/{id}` | `If-None-Match` | Allows a fresh client cache to receive 304 without transferring the representation. |
| `POST /orders/{id}/cancellation` | Do not blindly retry | It is neither safe nor naturally idempotent; a repeat conflicts after cancellation. |
| `POST /carts/items` | Do not blindly retry | Repeating increases quantity, so it is neither safe nor idempotent. |

## Complete HTTP exchange

**Request (HTTP/1.1):**

```http
POST /orders HTTP/1.1
Host: localhost:8081
Authorization: Bearer campus-eats-token
Accept: application/json
Content-Type: application/json
Idempotency-Key: demo-create-001
Content-Length: 64

{"studentId":17,"items":[{"itemId":101,"quantity":2}]}
```

**Response:**

```http
HTTP/1.1 201 CREATED
Content-Type: application/json
Location: /orders/1
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 99
X-Content-Type-Options: nosniff
Strict-Transport-Security: max-age=31536000; includeSubDomains
Access-Control-Allow-Origin: https://campuseats.example

{"id":1,"items":[{"itemId":101,"quantity":2}],"status":"placed","studentId":17}
```

## Required answers

1. `POST /orders` succeeds with **201** and `Location`, which tells the client the URI of the newly created order. `GET /orders/{id}` succeeds with **200** and `ETag`, which identifies the exact cached representation. `PUT /orders/{id}` succeeds with **200** and a new `ETag`, which lets the client make its next conditional update safely.

2. Both GET endpoints and OPTIONS are safe and idempotent. PUT is idempotent but not safe. The POST endpoints are not safe; cancellation and cart addition are also not naturally idempotent. `POST /orders` is neither by HTTP semantics, but the idempotency key makes retries safe from duplicate order creation and duplicate payment.

3. Example ETag: `"b50e..."` (the SHA-256 value returned by `GET /orders/1`). Sending it as `If-None-Match` returns **304 Not Modified** with no body, saving a JSON transfer. Sending an old value as `If-Match` on PUT returns **412 Precondition Failed**, preventing a stale editor from clobbering a newer order.

4. `POST /orders` with `{"studentId":"17","items":[]}` returns **400** because the request representation is malformed for the API contract. A syntactically valid order whose payment provider refuses the payment returns **422** because the request is understood but fails a business rule.

5. The browser blocks JavaScript from reading the response; the server can still log a 200 because CORS is enforced by the browser, not the API. `Access-Control-Allow-Origin: https://campuseats.example` fixes the permitted cross-origin request (and OPTIONS provides the preflight headers).

6. `GET /orders/{id}` uses `Cache-Control: public, max-age=60` because a read can be reused briefly and is validated by ETag. `PUT /orders/{id}` uses `Cache-Control: no-store` because a write response may reflect sensitive/current state and must not be stored.

7. Search stays GET when filters fit safely in a URL and the result is a shareable, cacheable read. POST is appropriate for a very large or structured/sensitive search payload that would exceed practical URL limits. Switching loses ordinary URL bookmarking, transparent cache behavior, and simple link sharing.

8. On **201**, `Location` points to the newly created resource (for example `/orders/1`). On a **3xx** response it points to the URI the client should request next.

## Production notes

The development server supplies `Date` and `Server` automatically. In production the API is served
only over HTTPS, so HSTS is meaningful to browsers. The Flask stack used here does not add gzip by
default; a production reverse proxy should negotiate `Content-Encoding: gzip` for large JSON bodies.
