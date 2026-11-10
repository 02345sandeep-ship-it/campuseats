# CampusEats Secured Menu/Catalogue REST API — CS543 Assignment 9

**Course:** CS543 — Web Services  
**Assignment:** 9 of 12 — Securing the API  
**Base service:** CampusEats Menu/Catalogue REST API from Assignment 8  
**Technology:** Node.js, Express, bcryptjs, JWT, dotenv

This project applies **only the Assignment 9 security requirements** to the existing Assignment 8 CampusEats catalogue. It keeps the original in-memory menu and its routes, adds login/JWT authentication, and adds role-based protection to the write route.

## Team details

Replace the placeholders before submission.

| Full name | Roll number |
|---|---|
| SANDEEP GUPTA | 20252651045 |
| DEEPANKAR BEJ | 20252651018 |
| RIKAM GOUDA | 20252651040 |
| SHIVAM RAJPUT | 20252651052 |

## 1. Requirements

- Node.js 18 or newer and npm.
- VS Code.
- Postman or curl.
- The project uses the original Assignment 8 in-memory catalogue. No database is needed.

## 2. Run on Windows (Command Prompt or VS Code terminal)

1. Extract this ZIP.
2. Open the extracted `CS543_A9_CampusEats_Secured` folder in VS Code (the folder containing `server.js` and `package.json`).
3. Open Terminal → New Terminal.
4. Install packages:

   ```cmd
   npm install
   ```

5. Create your local `.env` file from the example. In **Command Prompt (CMD)** use:

   ```cmd
   copy .env.example .env
   ```

   In **PowerShell**, the equivalent is:

   ```powershell
   Copy-Item .env.example .env
   ```

6. Open `.env` and set a private JWT secret, for example:

   ```env
   JWT_SECRET=replace_this_with_a_long_random_secret
   ```

   Keep `.env` private. It is git-ignored. Do not commit it or share its secret.

7. Start the server:

   ```cmd
   npm start
   ```

   Expected startup message:

   ```text
   CampusEats Secured API running at http://localhost:3000
   Routes: POST /login | GET /items | GET /items/:id | POST /items
   ```

8. Open the frontend at **http://localhost:3000**. Login first to view the protected catalogue.
9. Stop the server with `Ctrl + C`.

## 3. Demo users

Two users are seeded in memory with different roles. Their passwords are stored as bcrypt hashes, not plain-text password fields.

| Username | Demo password | Role | Permission |
|---|---|---|---|
| `customer` | `customer123` | `customer` | Read catalogue |
| `restaurant` | `restaurant123` | `restaurant` | Read catalogue and create menu items |

These are assignment demo credentials. Change them if you use the project beyond the classroom demo. Password hashes are generated with `bcrypt.hashSync` when the server starts.

## 4. Routes and access rules

| Method | Path | Guard(s) | Allowed role | Result |
|---|---|---|---|---|
| POST | `/login` | Login credential check | Valid seeded user | `200` with JWT; `401` on failed login |
| GET | `/items` | `auth` | Any authenticated user | `200` |
| GET | `/items/:id` | `auth` | Any authenticated user | `200`; `404` if missing |
| POST | `/items` | `auth`, then `requireRole('restaurant', 'admin')` | `restaurant` or `admin` | `201`; `403` for customer |

The catalogue remains in memory, as in Assignment 8. Restarting the server resets it to the four initial dishes.

## 5. API testing / Assignment 9 demonstration

Base URL: `http://localhost:3000`

### Case 1 — Request without token → 401

Run in CMD:

```cmd
curl -i http://localhost:3000/items
```

Expected: `401 Unauthorized`, JSON `{"error":"invalid token"}`. The route requires authentication and no Bearer token was supplied.

### Case 2 — Successful login → token

Restaurant login:

```cmd
curl -i -X POST http://localhost:3000/login -H "Content-Type: application/json" -d "{\"username\":\"restaurant\",\"password\":\"restaurant123\"}"
```

Expected: `200 OK` with a JWT in the `token` field. Copy the token value for the next requests.

Customer login (for the role-denial demonstration):

```cmd
curl -i -X POST http://localhost:3000/login -H "Content-Type: application/json" -d "{\"username\":\"customer\",\"password\":\"customer123\"}"
```

### Case 3 — Request with valid token → 200

Replace `PASTE_TOKEN_HERE` with the token from the successful login:

```cmd
curl -i http://localhost:3000/items -H "Authorization: Bearer PASTE_TOKEN_HERE"
```

Expected: `200 OK` and the menu JSON.

### Case 4 — Privileged restaurant role creates item → 201

Use the restaurant token:

```cmd
curl -i -X POST http://localhost:3000/items -H "Authorization: Bearer PASTE_RESTAURANT_TOKEN_HERE" -H "Content-Type: application/json" -d "{\"name\":\"Chole Bhature\",\"price\":80,\"available\":true}"
```

Expected: `201 Created` and the newly created item.

### Case 5 — Customer attempts write → 403

Use the customer token:

```cmd
curl -i -X POST http://localhost:3000/items -H "Authorization: Bearer PASTE_CUSTOMER_TOKEN_HERE" -H "Content-Type: application/json" -d "{\"name\":\"Customer Dish\",\"price\":50,\"available\":true}"
```

Expected: `403 Forbidden`, JSON `{"error":"forbidden"}`. The customer is authenticated, but the role is not allowed to write.

Also test invalid login (wrong username/password) and missing, invalid, or expired token; these return `401`.

## 6. Assignment 9 README answers

### Q1. Which routes require only authentication, and which also require a role?

- `GET /items` — authentication only (`auth`); any valid logged-in user.
- `GET /items/:id` — authentication only (`auth`); any valid logged-in user.
- `POST /items` — authentication followed by role authorization (`auth`, `requireRole('restaurant', 'admin')`); only restaurant/admin.
- `POST /login` — validates credentials and issues a token; it is not behind `auth`.

### Q2. Show one 401 and one 403. Why did the server return that code?

- **401:** `GET /items` without `Authorization: Bearer <token>` returns `401` because the caller has not supplied a valid authentication token.
- **403:** `POST /items` using a valid customer token returns `403` because the customer is authenticated but lacks the restaurant/admin role required to create menu items.

Capture the actual response in Postman or a terminal during your demo.

### Q3. What is inside the JWT payload? Why is the role claim safe to trust, and why must the secret stay out of code?

The JWT payload contains the user ID (`userId`) and role (`role`). The server verifies the JWT signature using its secret before using the role claim, so a client cannot simply alter the claim and produce a valid signed token. The secret must remain outside source code to prevent anyone who obtains the code from signing forged tokens. The secret is read from `process.env.JWT_SECRET`.

## 7. What was added for Assignment 9

- `POST /login` with `bcrypt.compareSync` and JWT signing with `expiresIn`.
- Two seeded users with different roles and bcrypt password hashes.
- `auth` middleware that extracts and verifies the Bearer token with `jwt.verify`; missing/invalid/expired tokens return `401`.
- `requireRole(...)` middleware; unauthorized authenticated users receive `403`.
- `auth` on catalogue GET routes and `auth` followed by role guard on `POST /items`.
- `.env.example` with a blank `JWT_SECRET`; `.env` is ignored by Git.
- Frontend login form that sends the token with protected requests.

## 8. Submission checklist

- [ ] Replace team placeholders with names and roll numbers.
- [ ] Push the project to GitHub. Ensure `.env` and `node_modules/` are not committed.
- [ ] Capture screenshots for the five demonstration cases: `401`, successful login/token, authenticated `200`, restaurant write `201`, customer write `403`.
- [ ] Record the short demo video and upload it with screenshots to Google Drive.
- [ ] Set the Drive link so the instructor can view it.
- [ ] Submit the GitHub repository and Drive links through Google Classroom (one submission per team).

## 9. Project structure

```text
CS543_A9_CampusEats_Secured/
├── server.js
├── package.json
├── package-lock.json       # created by npm install
├── .env.example
├── .gitignore              # ignores .env and node_modules
├── README.md
├── API-TESTING.md
├── public/
│   ├── index.html
│   └── style.css
├── postman/
│   └── CampusEats-Assignment-8.postman_collection.json
└── professor-starter-original/
    └── Assignment 8 starter files (reference only)
```

Run the main project from the top-level folder, not from `professor-starter-original`.
