# CS543 Web Services — Assignment 7: GraphQL

## Team members

Verified from the existing CampusEats README and assignment documentation:

| Name | Roll number |
| --- | --- |
| Sandeep Gupta | 20252651045 |
| Deepankar Bej | 20252651018 |
| Rikam Gouda | 20252651040 |
| Shivam Rajput | 20252651052 |

## Selected service and architecture

This submission adds a Dishes/Menu service. A browser page sends GraphQL queries and mutations with `fetch()` to Apollo Server at `/graphql`; resolvers in `server.js` call parameterized SQL helpers in `db.js`; MySQL stores the dishes. The service is isolated under `services/graphql` and does not replace the existing Orders or Payments services.

Stack: Node.js, Apollo Server 5, GraphQL, Express, `mysql2`, MySQL, and plain HTML/CSS/JavaScript.

```text
services/graphql/
├── db.js
├── schema.graphql
├── schema.sql
├── server.js
├── test/service.test.js
├── public/index.html
├── package.json
└── .env.example
```

## Setup and run

Requirements: Node.js 20+ and MySQL 8+. This project was prepared on Windows with Node.js 24.20.0, npm 11.19.0, and a running MySQL 8.0 Windows service. In PowerShell, from the repository root:

```powershell
cd services/graphql
npm install
Copy-Item .env.example .env
```

Edit `.env` with the local MySQL host, user, password, database, and optional port. The example targets `campuseats_graphql`. Using an authorized MySQL admin account, create the app database and local service account with a password you choose:

```sql
CREATE DATABASE campuseats_graphql CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
CREATE USER 'campuseats'@'127.0.0.1' IDENTIFIED BY 'choose-your-local-password';
GRANT ALL PRIVILEGES ON campuseats_graphql.* TO 'campuseats'@'127.0.0.1';
```

Set that same password in `.env`. Create the table and four initial records by running the schema initialization script; it prompts for the MySQL administrator login:

```powershell
npm run db:init
```

Check or start the MySQL Windows service from an elevated PowerShell window with `Get-Service MySQL80` and `Start-Service MySQL80`. Start with `npm run demo` (checks the MySQL TCP port and does not attempt to start MySQL) or `npm start`. Startup verifies database credentials and access before opening the HTTP port and prints both URLs. Open the frontend at <http://localhost:4000/>; the GraphQL endpoint is <http://localhost:4000/graphql>. Set `NODE_ENV=production` to disable introspection. Stop with Ctrl+C. Existing REST Orders and Payments services remain independent.

## Operations

```graphql
query {
  dishes {
    id
    name
    price
    available
  }
}
```

```graphql
query {
  dish(id: 1) {
    id
    name
    price
    available
  }
}
```

```graphql
mutation {
  addDish(input: { name: "Paneer Roll", price: 90 }) {
    id
    name
    price
    available
  }
}
```

### Required assignment questions

1. **Which CampusEats service did you pick?** The Dishes/Menu service, for listing menu items and adding a dish.
2. **Name one field a client can skip and one it cannot, and explain `!`.** A client can skip requesting `available` in a Dish selection set; GraphQL returns only selected fields. A client cannot omit `name` from `AddDishInput`, because its input field is `name: String!`. The `!` marks the input as required and guarantees selected output fields such as Dish `name` are non-null; returning null for one is an execution error.
3. **How does GraphQL map to SQL?** `dish(id: ID!)` invokes `Query.dish` in `server.js`, which calls `db.getDish(id)`; the parameterized `WHERE id = ?` in `db.js` receives that GraphQL ID. `addDish` invokes `Mutation.addDish`, validates the input, and calls `db.insertDish`; that function executes parameterized `INSERT INTO dishes ... VALUES (?, ?, TRUE)` and reads the inserted row back. The list resolver issues a SELECT without a WHERE clause.

## Tests and limitations

Run checks from `services/graphql`:

```powershell
npm test
```

Schema parsing and input validation tests do not require MySQL. SQL checks are skipped by default. To opt in, initialize the isolated test schema with `npm run db:test:init`, then grant the configured service user access to it:

```sql
GRANT ALL PRIVILEGES ON campuseats_graphql_test.* TO 'campuseats'@'127.0.0.1';
```

Run the integration checks from PowerShell without changing the `.env` application database:

```powershell
$env:DB_NAME = 'campuseats_graphql_test'
$env:RUN_DB_INTEGRATION = '1'
npm test
Remove-Item Env:DB_NAME, Env:RUN_DB_INTEGRATION
```

The mutation check deletes only its uniquely named test row; the failure check attempts port 1. Never point integration tests at the application database.

Preparation checks on this laptop: `npm ci` succeeded; `npm test` reported 2 passed, 0 failed, 2 skipped (the isolated MySQL checks); `npm audit` reported 0 vulnerabilities; Node syntax and both PowerShell script parses passed. MySQL 8.0 is running and accepts TCP on port 3306, but authentication could not be verified because no local service-account credentials are configured. A passwordless root check returned `ER_ACCESS_DENIED_ERROR`. The app correctly refuses startup until credentials and schema are available. The actual seeded query, database mutation, refresh persistence, and Chrome interaction therefore remain to be verified after local setup.

## Demonstration and submission media

Follow [DEMO_SCRIPT.md](DEMO_SCRIPT.md) for the 60–120 second recording steps. Save genuine before/after screenshots in this directory and upload the actual captures/video to the course submission location. No screenshot, video, or link is included unless captured from the running app.
