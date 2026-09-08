# CS543 Web Services — Assignment 4

# Rebuilding a CampusEats Service in REST

## Team Members

1. Sandeep Gupta - 20252651045
2. Deepankar Bej - 20252651018
3. Rikam Gouda - 20252651040
4. Shivam Rajput - 20252651052

## Part A — Model the Service

### A1 — Selected Service

**Orders**

The Orders service is responsible for managing carts, orders, and order status. This follows the service boundary and data ownership defined in Assignment 2 and does not redesign that boundary.

### A2 — SOAP-style Operations

| Operation | Purpose |
|---|---|
| `addToCart(...)` | Add an item to a student's cart |
| `placeOrder(...)` | Create/place an order |
| `getOrder(...)` | Retrieve an order |
| `cancelOrder(...)` | Cancel an order |

### A3 — REST Resources

| SOAP-style Operation | Durable Resource |
|---|---|
| `addToCart(...)` | `carts` |
| `placeOrder(...)` | `orders` |
| `getOrder(...)` | `orders` |
| `cancelOrder(...)` | `cancellations` |

The REST design uses nouns as resources rather than carrying the SOAP operation verbs into the URLs. Orders are the main durable resource, while cancellation is represented as a sub-resource of an order.

### A4 — Resource Table

| Method | URL | What it does | Success Code | Failure Codes |
|---|---|---|---|---|
| POST | `/carts/items` | Add an item to a student's cart | 201 | 400, 404, 409 |
| POST | `/orders` | Create an order | 201 | 400, 409, 422, 503 |
| GET | `/orders/{id}` | Read one order | 200 | 404 |
| GET | `/orders?studentId={id}` | List orders for a student | 200 | 400 |
| POST | `/orders/{id}/cancellation` | Start cancellation of an order | 202 | 404, 409 |

### A5 — Hard Choice

The least comfortable operation to map was `cancelOrder(orderId)` because cancellation is a state-changing action rather than a durable order resource. I represented it as the `cancellation` sub-resource of an order using `POST /orders/{id}/cancellation`. This keeps the order itself as the primary resource while clearly expressing the state-changing operation. I rejected an action-style URL such as `/cancelOrder` because resource URLs should use nouns rather than verbs.

---

# Part D — Fallback

### D3 — Fallback Reasoning

If the Payments service is unreachable while creating an order, the Orders service will fail the request with `503 Service Unavailable` rather than creating an order without successful payment. Degrading in this case would be incorrect because it could leave an order created without its required payment and create inconsistent service state.

---

# Comparison with Assignment 3

## 1. WSDL line count vs OpenAPI line count

The Assignment 3 `partner.wsdl` contains **153 lines**. The Assignment 4 `openapi.yaml` contains **316 lines**.

The OpenAPI file is longer because it documents five endpoints with full request/response schemas, reusable error responses, and parameter definitions. The WSDL only described a single `charge` operation.

Two things the WSDL had that OpenAPI does not:

1. **`<binding>`** — declared the SOAP-over-HTTP transport and document style. REST uses HTTP methods and URLs directly, so no binding element is needed.
2. **`<port>` inside `<service>`** — linked the binding to a specific SOAP endpoint address. In OpenAPI the server URL is just a top-level `servers` field.

---

## 2. SOAP Fault replaced by an HTTP error

In Assignment 3, the SOAP fault contained:

> `<faultstring>Card declined</faultstring>`

and:

> `<uni:error code="card_declined"/>`

The REST version represents the same business failure with HTTP status **422 Unprocessable Entity** and a Problem JSON body:

```json
{
  "type": "/errors/payment-refused",
  "title": "Payment refused",
  "status": 422,
  "detail": "The payment service refused the payment."
}
```

Returning 200 for this case would be wrong because the HTTP status code is how REST clients detect success vs failure. A 200 response means the request succeeded, which would mislead the client into thinking the order was placed. The status code is the first thing intermediaries and client libraries check, so it must reflect the actual outcome.

---

## 3. UDDI → REST/OpenAPI equivalents

- **UDDI publish** — The service provider registers its WSDL in a UDDI registry so others can discover it. In REST, the equivalent is publishing an OpenAPI spec file, hosting it at a well-known URL, or listing the API in a developer portal or API gateway.

- **UDDI find** — A consumer searches the UDDI registry by name, category, or binding to locate a service. In REST, the equivalent is browsing a developer portal, searching an API catalog, or simply knowing the service URL and reading its OpenAPI spec.

- **UDDI bind** — The consumer retrieves the WSDL endpoint from UDDI and configures its client to call that address. In REST, the equivalent is reading the `servers.url` from the OpenAPI spec and pointing the HTTP client at that base URL.

---

## 4. Validation function replacing XML Schema

The validation function in the Orders service is **`validate_order`** (in `app.py`). It checks that `studentId` is a positive integer, `items` is a non-empty list, and each item has a valid `itemId` and `quantity`.

Example of malformed input:

```json
{
  "studentId": -1,
  "items": [{"itemId": 101, "quantity": 2}]
}
```

The service returns **400 Bad Request** with a Problem JSON body:

```json
{
  "type": "/errors/invalid-request",
  "title": "Invalid request",
  "status": 400,
  "detail": "studentId must be greater than 0."
}
```

There is also a **`validate_cart`** function for the `POST /carts/items` endpoint that performs similar checks on `studentId`, `itemId`, and `quantity`.

---

## 5. Where SOAP is still a reasonable choice

SOAP is still a reasonable choice in **banking and financial transaction systems** where WS-Security and WS-ReliableMessaging are needed. SOAP provides built-in standards for message-level encryption, digital signatures, and guaranteed delivery, which are important when messages pass through multiple intermediaries. REST has no built-in equivalent of these WS-* standards and would require assembling separate solutions for each guarantee.

---

# Manual Validation

The Orders service was run on port **8081** and the Payments service was run on port **8082**.

## 1. Health check

```powershell
Invoke-RestMethod -Uri http://localhost:8081/health -Method GET
```

Expected: `{"status": "ok"}`

## 2. Add cart item

```powershell
Invoke-RestMethod -Uri http://localhost:8081/carts/items -Method POST -ContentType "application/json" -Body '{"studentId": 17, "itemId": 101, "quantity": 2}'
```

Expected: 201 with cart data.

## 3. Create order (success — requires Payments running)

```powershell
Invoke-RestMethod -Uri http://localhost:8081/orders -Method POST -ContentType "application/json" -Headers @{"Idempotency-Key"="order-test-001"} -Body '{"studentId": 17, "items": [{"itemId": 101, "quantity": 2}]}'
```

Expected: 201 with order data.

## 4. Repeat create order with same Idempotency-Key

```powershell
Invoke-RestMethod -Uri http://localhost:8081/orders -Method POST -ContentType "application/json" -Headers @{"Idempotency-Key"="order-test-001"} -Body '{"studentId": 17, "items": [{"itemId": 101, "quantity": 2}]}'
```

Expected: Same order returned, no duplicate created.

## 5. Get order

```powershell
Invoke-RestMethod -Uri http://localhost:8081/orders/1 -Method GET
```

Expected: 200 with order data.

## 6. List orders

```powershell
Invoke-RestMethod -Uri "http://localhost:8081/orders?studentId=17" -Method GET
```

Expected: 200 with array of orders.

## 7. Cancel order

```powershell
Invoke-RestMethod -Uri http://localhost:8081/orders/1/cancellation -Method POST
```

Expected: 202 with order status changed to `"cancelled"`.

## 8. Unknown order → 404

```powershell
Invoke-RestMethod -Uri http://localhost:8081/orders/999 -Method GET
```

Expected: 404 with Problem JSON.

## 9. Missing/invalid input → 400

```powershell
Invoke-RestMethod -Uri http://localhost:8081/orders -Method POST -ContentType "application/json" -Headers @{"Idempotency-Key"="key-bad"} -Body '{"studentId": "abc"}'
```

Expected: 400 with Problem JSON.

## 10. Payment unavailable → 503

Stop the Payments service, then:

```powershell
Invoke-RestMethod -Uri http://localhost:8081/orders -Method POST -ContentType "application/json" -Headers @{"Idempotency-Key"="key-503"} -Body '{"studentId": 17, "items": [{"itemId": 101, "quantity": 2}]}'
```

Expected: 503 with Problem JSON after retries are exhausted.

## 11. Payment refused → 422

Configure Payments to refuse the charge (return 4xx), then:

```powershell
Invoke-RestMethod -Uri http://localhost:8081/orders -Method POST -ContentType "application/json" -Headers @{"Idempotency-Key"="key-422"} -Body '{"studentId": 17, "items": [{"itemId": 101, "quantity": 2}]}'
```

Expected: 422 with Problem JSON.

---

# curl -i Transcript

The following transcript was captured from the running Orders service using `curl.exe -i`.

## 1. Successful order creation

```text
PS D:\Classroom\3rd Sem\Web Services\CampusEats\campuseats> curl.exe -i -X POST "http://localhost:8081/orders" -H "Content-Type: application/json" -H "Idempotency-Key: curl-test-001" --data-binary "@order.json"

HTTP/1.1 201 CREATED
Server: Werkzeug/3.1.8 Python/3.14.7
Date: Tue, 08 Sep 2026 17:20:38 GMT
Content-Type: application/json
Content-Length: 80
Location: /orders/1
Connection: close

{"id":1,"items":[{"itemId":101,"quantity":2}],"status":"placed","studentId":17}
```

## 2. Same request with the same Idempotency-Key

```text
PS D:\Classroom\3rd Sem\Web Services\CampusEats\campuseats> curl.exe -i -X POST "http://localhost:8081/orders" -H "Content-Type: application/json" -H "Idempotency-Key: curl-test-001" --data-binary "@order.json"

HTTP/1.1 201 CREATED
Server: Werkzeug/3.1.8 Python/3.14.7
Date: Tue, 08 Sep 2026 17:21:10 GMT
Content-Type: application/json
Content-Length: 80
Location: /orders/1
Connection: close

{"id":1,"items":[{"itemId":101,"quantity":2}],"status":"placed","studentId":17}
```

The same order ID (`1`) was returned, showing that the request did not create a duplicate order.

## 3. Malformed request body

```text
PS D:\Classroom\3rd Sem\Web Services\CampusEats\campuseats> curl.exe -i -X POST "http://localhost:8081/orders" -H "Content-Type: application/json" -H "Idempotency-Key: curl-bad-001" --data-raw "hello"

HTTP/1.1 400 BAD REQUEST
Server: Werkzeug/3.1.8 Python/3.14.7
Date: Tue, 08 Sep 2026 17:21:35 GMT
Content-Type: application/json
Content-Length: 121
Connection: close

{"detail":"Request body must be a JSON object.","status":400,"title":"Invalid request","type":"/errors/invalid-request"}
```

## 4. Missing order

```text
PS D:\Classroom\3rd Sem\Web Services\CampusEats\campuseats> curl.exe -i "http://localhost:8081/orders/9999"

HTTP/1.1 404 NOT FOUND
Server: Werkzeug/3.1.8 Python/3.14.7
Date: Tue, 08 Sep 2026 17:22:06 GMT
Content-Type: application/json
Content-Length: 115
Connection: close

{"detail":"No order exists with id 9999.","status":404,"title":"Order not found","type":"/errors/order-not-found"}
```

## 5. Cancel order

```text
PS D:\Classroom\3rd Sem\Web Services\CampusEats\campuseats> curl.exe -i -X POST "http://localhost:8081/orders/1/cancellation"

HTTP/1.1 202 ACCEPTED
Server: Werkzeug/3.1.8 Python/3.14.7
Date: Tue, 08 Sep 2026 17:22:38 GMT
Content-Type: application/json
Content-Length: 83
Connection: close

{"id":1,"items":[{"itemId":101,"quantity":2}],"status":"cancelled","studentId":17}
```

## 6. Cancel the already-cancelled order

```text
PS D:\Classroom\3rd Sem\Web Services\CampusEats\campuseats> curl.exe -i -X POST "http://localhost:8081/orders/1/cancellation"

HTTP/1.1 409 CONFLICT
Server: Werkzeug/3.1.8 Python/3.14.7
Date: Tue, 08 Sep 2026 17:23:49 GMT
Content-Type: application/json
Content-Length: 139
Connection: close

{"detail":"The order has already been cancelled.","status":409,"title":"Order already cancelled","type":"/errors/order-already-cancelled"}
```

## Validation Summary

| Test | HTTP Result |
|---|---|
| Successful order creation | 201 Created |
| Same Idempotency-Key | 201 Created, same order ID |
| Malformed request body | 400 Bad Request |
| Missing order | 404 Not Found |
| Cancel order | 202 Accepted |
| Cancel already-cancelled order | 409 Conflict |
