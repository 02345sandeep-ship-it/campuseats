# HTTP Request/Response Log

## Request 1 — Get User 1

### Command

curl.exe -i https://jsonplaceholder.typicode.com/users/1

### Response

HTTP/1.1 200 OK
Date: Sat, 15 Aug 2026 14:38:34 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 509
Connection: keep-alive
access-control-allow-credentials: true
Cache-Control: max-age=43200
etag: W/"1fd-+2Y3G3w049iSZtw5t1mzSnunngE"
expires: -1
nel: {"report_to":"heroku-nel","response_headers":["Via"],"max_age":3600,"success_fraction":0.01,"failure_fraction":0.1}
pragma: no-cache
report-to: {"group":"heroku-nel","endpoints":[{"url":"https://nel.heroku.com/reports?s=6DQIIPkCgnZS0mG6n6a1gC5gfYOBpO568WJCudBefYY%3D\u0026sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d\u0026ts=1786671173"}],"max_age":3600}
reporting-endpoints: heroku-nel="https://nel.heroku.com/reports?s=6DQIIPkCgnZS0mG6n6a1gC5gfYOBpO568WJCudBefYY%3D&sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d&ts=1786671173"
Server: cloudflare
vary: Origin, Accept-Encoding
via: 2.0 heroku-router
x-content-type-options: nosniff
x-powered-by: Express
x-ratelimit-limit: 1000
x-ratelimit-remaining: 999
x-ratelimit-reset: 1786671192
Age: 18058
Accept-Ranges: bytes
cf-cache-status: HIT
CF-RAY: a2b8f19c0e6f18fc-BOM
alt-svc: h3=":443"; ma=86400

{
  "id": 1,
  "name": "Leanne Graham",
  "username": "Bret",
  "email": "Sincere@april.biz",
  "address": {
    "street": "Kulas Light",
    "suite": "Apt. 556",
    "city": "Gwenborough",
    "zipcode": "92998-3874",
    "geo": {
      "lat": "-37.3159",
      "lng": "81.1496"
    }
  },
  "phone": "1-770-736-8031 x56442",
  "website": "hildegard.org",
  "company": {
    "name": "Romaguera-Crona",
    "catchPhrase": "Multi-layered client-server neural-net",
    "bs": "harness real-time e-markets"
  }
}

### Explanation

- Status: 200 OK — The server successfully processed the request and returned the requested user.
- Content-Type: application/json; charset=utf-8 — The response body is JSON data encoded using UTF-8.


## Request 2 — Get User 2

### Command

curl.exe -i https://jsonplaceholder.typicode.com/users/2

### Response

HTTP/1.1 200 OK
Date: Sat, 15 Aug 2026 14:41:41 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 509
Connection: keep-alive
access-control-allow-credentials: true
Cache-Control: max-age=43200
etag: W/"1fd-XTG63SYhaP/Uo6/vgmARnL3rpBk"
expires: -1
nel: {"report_to":"heroku-nel","response_headers":["Via"],"max_age":3600,"success_fraction":0.01,"failure_fraction":0.1}
pragma: no-cache
report-to: {"group":"heroku-nel","endpoints":[{"url":"https://nel.heroku.com/reports?s=z9GIac45CJ67HGWNia17l%2Blytj3uxzPrFKduQqLCzMk%3D\u0026sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d\u0026ts=1786786623"}],"max_age":3600}
reporting-endpoints: heroku-nel="https://nel.heroku.com/reports?s=z9GIac45CJ67HGWNia17l%2Blytj3uxzPrFKduQqLCzMk%3D&sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d&ts=1786786623"
Server: cloudflare
vary: Origin, Accept-Encoding
via: 2.0 heroku-router
x-content-type-options: nosniff
x-powered-by: Express
x-ratelimit-limit: 1000
x-ratelimit-remaining: 912
x-ratelimit-reset: 1786786663
Age: 18278
Accept-Ranges: bytes
cf-cache-status: HIT
CF-RAY: a2b8f62d4c713a99-BOM
alt-svc: h3=":443"; ma=86400

{
  "id": 2,
  "name": "Ervin Howell",
  "username": "Antonette",
  "email": "Shanna@melissa.tv",
  "address": {
    "street": "Victor Plains",
    "suite": "Suite 879",
    "city": "Wisokyburgh",
    "zipcode": "90566-7771",
    "geo": {
      "lat": "-43.9509",
      "lng": "-34.4618"
    }
  },
  "phone": "010-692-6593 x09125",
  "website": "anastasia.net",
  "company": {
    "name": "Deckow-Crist",
    "catchPhrase": "Proactive didactic contingency",
    "bs": "synergize scalable supply-chains"
  }
}

### Explanation

- Status: 200 OK — The server successfully processed the request and returned the requested user.
- Content-Type: application/json; charset=utf-8 — The response body is JSON data encoded using UTF-8.


## Request 3 — Get Post 1

### Command

curl.exe -i https://jsonplaceholder.typicode.com/posts/1

### Response

HTTP/1.1 200 OK
Date: Sat, 15 Aug 2026 14:44:19 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 292
Connection: keep-alive
access-control-allow-credentials: true
Cache-Control: max-age=43200
etag: W/"124-yiKdLzqO5gfBrJFrcdJ8Yq0LGnU"
expires: -1
nel: {"report_to":"heroku-nel","response_headers":["Via"],"max_age":3600,"success_fraction":0.01,"failure_fraction":0.1}
pragma: no-cache
report-to: {"group":"heroku-nel","endpoints":[{"url":"https://nel.heroku.com/reports?s=vm67FVLNHsCgrFgubRa04ooDeMKdgwXS9H3i2IbjuoY%3D\u0026sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d\u0026ts=1785194657"}],"max_age":3600}
reporting-endpoints: heroku-nel="https://nel.heroku.com/reports?s=vm67FVLNHsCgrFgubRa04ooDeMKdgwXS9H3i2IbjuoY%3D&sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d&ts=1785194657"
Server: cloudflare
vary: Origin, Accept-Encoding
via: 2.0 heroku-router
x-content-type-options: nosniff
x-powered-by: Express
x-ratelimit-limit: 1000
x-ratelimit-remaining: 999
x-ratelimit-reset: 1785194663
Age: 26364
Accept-Ranges: bytes
cf-cache-status: HIT
CF-RAY: a2b8fa02dfdf94dd-BOM
alt-svc: h3=":443"; ma=86400

{
  "userId": 1,
  "id": 1,
  "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
  "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
}

### Explanation

- Status: 200 OK — The server successfully processed the request and returned post 1.
- Content-Type: application/json; charset=utf-8 — The response body is JSON data encoded using UTF-8.


## Request 4 — Get Post 2

### Command

curl.exe -i https://jsonplaceholder.typicode.com/posts/2

### Response

HTTP/1.1 200 OK
Date: Sat, 15 Aug 2026 14:45:55 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 278
Connection: keep-alive
access-control-allow-credentials: true
Cache-Control: max-age=43200
etag: W/"116-jnDuMpjju89+9j7e0BqkdFsVRjs"
expires: -1
nel: {"report_to":"heroku-nel","response_headers":["Via"],"max_age":3600,"success_fraction":0.01,"failure_fraction":0.1}
pragma: no-cache
report-to: {"group":"heroku-nel","endpoints":[{"url":"https://nel.heroku.com/reports?s=disGhkkkNNxGJPDcfLwwgv1elBmmV5U8fbfbKG6OTfU%3D\u0026sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d\u0026ts=1786775129"}],"max_age":3600}
reporting-endpoints: heroku-nel="https://nel.heroku.com/reports?s=disGhkkkNNxGJPDcfLwwgv1elBmmV5U8fbfbKG6OTfU%3D&sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d&ts=1786775129"
Server: cloudflare
vary: Origin, Accept-Encoding
via: 2.0 heroku-router
x-content-type-options: nosniff
x-powered-by: Express
x-ratelimit-limit: 1000
x-ratelimit-remaining: 808
x-ratelimit-reset: 1786775143
Age: 828
Accept-Ranges: bytes
cf-cache-status: HIT
CF-RAY: a2b8fc5d3bda4415-BOM
alt-svc: h3=":443"; ma=86400

{
  "userId": 1,
  "id": 2,
  "title": "qui est esse",
  "body": "est rerum tempore vitae\nsequi sint nihil reprehenderit dolor beatae ea dolores neque\nfugiat blanditiis voluptate porro vel nihil molestiae ut reiciendis\nqui aperiam non debitis possimus qui neque nisi nulla"
}

### Explanation

- Status: 200 OK — The server successfully processed the request and returned post 2.
- Content-Type: application/json; charset=utf-8 — The response body is JSON data encoded using UTF-8.


## Request 5 — Request for a Non-existent Post

### Command

curl.exe -i https://jsonplaceholder.typicode.com/posts/9999

### Response

HTTP/1.1 404 Not Found
Date: Sat, 15 Aug 2026 14:47:07 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 2
Connection: keep-alive
access-control-allow-credentials: true
Cache-Control: max-age=43200
etag: W/"2-vyGp6PvFo4RvsFtPoIWeCReyIC8"
expires: -1
nel: {"report_to":"heroku-nel","response_headers":["Via"],"max_age":3600,"success_fraction":0.01,"failure_fraction":0.1}
pragma: no-cache
report-to: {"group":"heroku-nel","endpoints":[{"url":"https://nel.heroku.com/reports?s=OTPv1x5hvtB%2BUkQvxLj%2BJbLo0HOiVaukzGFw1UT0Avk%3D\u0026sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d\u0026ts=1786790214"}],"max_age":3600}
reporting-endpoints: heroku-nel="https://nel.heroku.com/reports?s=OTPv1x5hvtB%2BUkQvxLj%2BJbLo0HOiVaukzGFw1UT0Avk%3D&sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d&ts=1786790214"
Server: cloudflare
vary: Origin
via: 2.0 heroku-router
x-content-type-options: nosniff
x-powered-by: Express
x-ratelimit-limit: 1000
x-ratelimit-remaining: 999
x-ratelimit-reset: 1786790263
Age: 15013
cf-cache-status: HIT
CF-RAY: a2b8fe221ca7ff64-BOM
alt-svc: h3=":443"; ma=86400

{}

### Explanation

- Status: 404 Not Found — The requested resource does not exist on the server.
- Content-Type: application/json; charset=utf-8 — The response is returned in JSON format using UTF-8 encoding.

## Summary

Five HTTP requests were made using curl.exe -i against a public read-only JSON API. Four requests returned 200 OK, and one deliberately requested a non-existent resource and returned 404 Not Found.