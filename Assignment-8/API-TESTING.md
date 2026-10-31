# API Testing Quick Reference — Assignment 8

Start the server in the project root first: `npm install` then `npm start`.

| Test | Method | URL | Expected status |
|---|---|---|---|
| List menu | GET | `http://localhost:3000/items` | 200 |
| Get item 1 | GET | `http://localhost:3000/items/1` | 200 |
| Missing item | GET | `http://localhost:3000/items/999` | 404 |
| Create item | POST | `http://localhost:3000/items` | 201 |
| Missing required name | POST | `http://localhost:3000/items` | 422 |

For POST, use Postman → Body → raw → JSON and header `Content-Type: application/json`.

Success body:

```json
{"name":"Chole Bhature","price":80,"available":true}
```

422 body:

```json
{"price":80,"available":true}
```

Expected 422 response: `{"error":"name required"}`.
