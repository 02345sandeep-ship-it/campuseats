# API Testing Quick Reference

Start the server first with `npm start`.

| Test | Method | URL | Expected |
|---|---|---|---|
| List all dishes | GET | `http://localhost:3000/items` | 200 + JSON array |
| Find dish 1 | GET | `http://localhost:3000/items/1` | 200 + Veg Thali |
| Unknown dish | GET | `http://localhost:3000/items/999` | 404 + `{"error":"not found"}` |
| Add dish | POST | `http://localhost:3000/items` | 201 + created item |
| Delete dish 3 | DELETE | `http://localhost:3000/items/3` | 204, empty body |

For POST in Postman: **Body → raw → JSON**:

```json
{
  "name": "Masala Dosa",
  "price": 60
}
```

For invalid POST test, send `{ "price": 60 }`; expected status is 422 and error is `name required`.

Data is stored in memory. Restarting the server resets the menu to the two starter dishes.
