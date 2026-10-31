# CampusEats Catalogue — CS543 Web Services Tutorial 08

A working Node.js + Express implementation of the professor's Catalogue starter project. The original starter files are preserved unchanged in `professor-starter-original/`.

## 1. Requirements

- Node.js 18 or newer (Node.js 20/22 LTS is recommended)
- npm (installed with Node.js)
- Visual Studio Code (or another editor)
- Postman (optional, for API testing)

Check installation in the VS Code terminal:

```powershell
node -v
npm -v
```

## 2. Open and run in VS Code (Windows)

1. Extract the ZIP file.
2. Open VS Code.
3. Select **File → Open Folder** and choose the extracted `catalogue` folder (the folder containing `server.js`).
4. Open **Terminal → New Terminal**.
5. Install dependencies:

   ```powershell
   npm install
   ```

6. Start the server:

   ```powershell
   npm start
   ```

7. Open this address in Chrome/Edge:

   `http://localhost:3000`

You should see the CampusEats Catalogue with **Veg Thali (₹90)** and **Paneer Roll (₹70)**. Add a dish using the form; it should appear in the list.

### Development mode (optional)

Run `npm run dev` to restart the server automatically when `server.js` changes. Stop either server with **Ctrl + C** in the terminal.

## 3. REST API endpoints

Base URL: `http://localhost:3000`

| Method | Endpoint | Purpose | Success status |
|---|---|---|---|
| GET | `/items` | Get all dishes | 200 OK |
| GET | `/items/1` | Get one dish by ID | 200 OK |
| POST | `/items` | Add a dish | 201 Created |
| DELETE | `/items/1` | Delete a dish by ID (extension) | 204 No Content |

Error responses include `400 Bad Request` for an invalid ID/JSON, `404 Not Found` for an unknown dish, and `422 Unprocessable Content` when the dish name or price is invalid.

## 4. Test APIs using Postman

Keep the Node server running while testing. Open Postman and create requests as follows.

### A. Get all dishes

- Method: `GET`
- URL: `http://localhost:3000/items`
- Click **Send**.
- Expected: status `200 OK` and a JSON array containing Veg Thali and Paneer Roll.

### B. Get one dish

- Method: `GET`
- URL: `http://localhost:3000/items/1`
- Click **Send**.
- Expected: status `200 OK` and Veg Thali JSON.

### C. Add a dish

- Method: `POST`
- URL: `http://localhost:3000/items`
- Open **Body → raw → JSON**.
- Enter:

  ```json
  {
    "name": "Masala Dosa",
    "price": 60
  }
  ```

- Click **Send**.
- Expected: status `201 Created` and the new item in the response.
- Send `GET http://localhost:3000/items` again to see the new dish.

### D. Delete a dish (extra practice)

- Method: `DELETE`
- URL: `http://localhost:3000/items/3` (use an ID that currently exists).
- Click **Send**.
- Expected: status `204 No Content`.
- Send `GET http://localhost:3000/items` to confirm it was removed.

### Import the included Postman collection

In Postman choose **Import → File**, then select `postman/CampusEats-API.postman_collection.json`. The collection contains GET all, GET by ID, POST, and DELETE examples. Run the requests while the server is running.

## 5. Test APIs from Windows PowerShell (alternative)

PowerShell has its own `curl` alias on some versions. Use `curl.exe` explicitly:

```powershell
curl.exe http://localhost:3000/items
curl.exe http://localhost:3000/items/1
curl.exe -X POST http://localhost:3000/items -H "Content-Type: application/json" -d '{"name":"Masala Dosa","price":60}'
curl.exe -i -X DELETE http://localhost:3000/items/3
```

## 6. Project structure

```text
catalogue/
├── server.js                         # Express REST API
├── package.json                      # Project scripts and Express dependency
├── README.md                         # Setup and run instructions
├── API-TESTING.md                    # Short API testing reference
├── .gitignore
├── postman/
│   └── CampusEats-API.postman_collection.json
├── public/
│   ├── index.html                    # Frontend + Fetch API calls
│   └── style.css                     # Responsive styling
└── professor-starter-original/       # Professor's supplied files, unchanged
    ├── server.js
    ├── package.json
    ├── README.md
    └── public/
        ├── index.html
        └── style.css
```

## 7. Important notes for the tutorial

- The browser page and API are served by the same Express server. The frontend uses `fetch('/items')`, so CORS configuration is not needed for this setup.
- The menu is stored in a JavaScript array in memory, as required by the tutorial. **New dishes and deletions are lost when the server stops/restarts.** This is intentional; the tutorial says a database will be introduced in Lecture 10.
- The supplied starter files have not been discarded: compare or run them from `professor-starter-original/` if your instructor wants to see the original version.
- The DELETE endpoint is an optional extension suggested at the end of the professor's PDF. The core tutorial requirements remain GET all, GET by ID, POST, and the HTML/CSS frontend.

## 8. Troubleshooting

- **`'node' is not recognized`:** Install Node.js, close and reopen VS Code, then check `node -v`.
- **`Cannot find module 'express'`:** Run `npm install` in the folder containing `package.json`.
- **Port 3000 is already in use:** Stop the other server with Ctrl+C, or use another port in PowerShell: `$env:PORT=3001; npm start` and open `http://localhost:3001`.
- **Browser shows `Cannot GET /`:** Make sure you started the server from the main `catalogue` folder and that `public/index.html` exists.
- **Menu stays on Loading:** Check that the terminal still shows the server running and open the site through `http://localhost:3000`, not by double-clicking the HTML file.

## 9. Viva preparation

- **What is Express?** A Node.js web framework used here to create HTTP routes.
- **What is REST API?** An interface that lets the frontend communicate with the backend using HTTP methods and URLs.
- **GET vs POST?** GET reads data; POST creates a new dish.
- **What is `req.params`?** It reads values from URL path parameters, such as the `1` in `/items/1`.
- **What is `req.body`?** It contains the JSON data sent by the client in a POST request.
- **Why `express.json()`?** It parses incoming JSON request bodies so they are available in `req.body`.
- **Why status 201?** It indicates that a resource was created successfully.
- **Why status 404?** The requested dish ID does not exist.
- **Why does data disappear after restart?** The array is stored in server memory, not a database.
