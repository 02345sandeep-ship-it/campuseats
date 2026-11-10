# CampusEats Assignment 9 — API Testing

Start the server with `npm install` and `npm start`. Base URL: `http://localhost:3000`.

## Login

**POST** `/login` with JSON:

```json
{"username":"restaurant","password":"restaurant123"}
```

Copy the returned `token`.

## Protected catalogue read

**GET** `/items`

Header:

```http
Authorization: Bearer <token>
```

A valid token returns `200`. Missing, invalid, or expired token returns `401`.

## Create menu item

**POST** `/items`

Headers:

```http
Authorization: Bearer <restaurant-token>
Content-Type: application/json
```

Body:

```json
{"name":"Chole Bhature","price":80,"available":true}
```

A restaurant/admin token returns `201`. A customer token returns `403`. A missing/invalid token returns `401`.

The full Windows CMD curl commands and the five Assignment 9 demo cases are in `README.md`.
