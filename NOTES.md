# CS543 Web Services — Assignment 6

## Outcome map

| Endpoint | Success | Failure statuses |
|---|---:|---|
| POST /orders | 201 + Location | 401, 406, 422, 429, 503 |
| GET /orders?studentId= | 200 | 401, 406, 422, 429 |
| GET /orders/{id} | 200 | 401, 404, 406, 429 |
| PATCH /orders/{id} | 200 | 401, 404, 406, 409, 422, 429 |
| DELETE /orders/{id} | 200 | 401, 404, 406, 409, 429 |

Every failure goes through problem() and has application/problem+json; charset=utf-8. Stable types include invalid-input, empty-cart, item-unavailable, payment-declined, order-not-found, and illegal-transition; operational types are unauthorized, not-acceptable, rate-limited, and payment-unavailable.

## Required answers

1. The status map above records every endpoint outcome. No error returns 200.
2. The stable types are listed above. General validation triggers invalid-input; an empty item list uses empty-cart and includes the field rule “must be a non-empty array”.
3. problem() in services/orders/errors.py builds every error body and sets the Problem Details media type.
4. Field-level validation returns 422 and errors[]; for example items[0].quantity must be at least 1.
5. Only POST with the same Idempotency-Key is safe to repeat after a network failure. A 429 or 503 supplies Retry-After; other 4xx responses require fixing the request, not retrying it.
6. Server exceptions are not returned to clients. The client gets a short public detail while diagnostic detail belongs in server-side logging.
7. The service produces JSON by default. Accept: application/xml receives 406 because XML is not offered.
