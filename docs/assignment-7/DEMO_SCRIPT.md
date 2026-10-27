# CampusEats Assignment 7 — 60–120 second demo

## Before recording

Configure MySQL and `.env` using [README.md](README.md). Then, from the repository root in Windows PowerShell:

```powershell
cd services/graphql
npm ci
npm run demo
```

If MySQL is stopped, use an elevated PowerShell window to start it with `Start-Service MySQL80`, then retry `npm run demo`. The demo script does not start MySQL or bypass credential/schema errors.

Open **http://localhost:4000/** in Chrome. The GraphQL API is **http://localhost:4000/graphql**.

## Recording sequence

1. Show the four seed dishes loaded in the CampusEats GraphQL menu.
2. Explain that the page sends `fetch()` requests to Apollo at `/graphql`, and SQL resolvers read/write MySQL.
3. Enter `Paneer Roll` and `90`, then click **Add to menu**.
4. Show the success message and the added dish with its generated ID.
5. Refresh Chrome and show that Paneer Roll remains in the menu.
6. Optionally show `/graphql` and run `{ dishes { id name price available } }` in the GraphQL explorer.

Capture genuine screenshots before adding the dish and after it appears, saving them as `docs/assignment-7/before.png` and `docs/assignment-7/after.png`. Record the flow with Windows Xbox Game Bar (**Win+Alt+R**) or another available recorder. Upload the actual captures/video to the course submission location and add the actual video link to the README; do not use synthetic images as application evidence.
