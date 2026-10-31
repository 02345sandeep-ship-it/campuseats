# CampusEats Menu/Catalogue REST API — CS543 Assignment 8

**Course:** CS543 — Web Services  
**Assignment:** 8 of 12  
**Selected Service:** Menu / Catalogue  
**Technologies:** Node.js, Express.js, HTML, CSS, JavaScript, Fetch API

## Team Members

| S.No. | Name | Roll Number |
|---|---|---|
| 1 | Sandeep Gupta | 20252651045 |
| 2 | Deepankar Bej | 20252651018 |
| 3 | Rikam Gouda | 20252651040 |
| 4 | Shivam Rajput | 20252651052 |

## 1. Project Overview

CampusEats Menu/Catalogue is a REST API-based web application developed using Node.js and Express.js.

The application allows users to view all food items, fetch an individual food item, and add new food items through a web interface.

The application uses an in-memory array to store menu records.

## 2. Technologies Used

- Node.js – Backend runtime environment.
- Express.js – REST API development.
- HTML – Webpage structure.
- CSS – User interface design.
- JavaScript – Frontend functionality.
- Fetch API – Communication between frontend and backend.
- Postman – REST API testing.

## 3. How to Run the Project

**Requirements:** Node.js, npm and Visual Studio Code.

1. Extract the project ZIP.
2. Open the project folder in VS Code.
3. Open Terminal → New Terminal.
4. Install dependencies:

```bash
npm install
```

5. Start the server:

```bash
npm start
```

6. Open the browser:

http://localhost:3000

The application will display the CampusEats food catalogue.

**Important:** Run commands from the main project folder containing `server.js` and `package.json`.

## 4. Initial Menu Data

The application starts with four food records.

| ID | Food Name | Price | Available |
|---|---|---:|---|
| 1 | Veg Thali | ₹90 | Yes |
| 2 | Paneer Roll | ₹70 | Yes |
| 3 | Masala Dosa | ₹60 | Yes |
| 4 | Veg Biryani | ₹120 | No |

The data is stored in an in-memory JavaScript array. Records added during execution reset when the server restarts.

## 5. REST API Endpoints

Base URL: `http://localhost:3000`

| HTTP Method | Endpoint | Description |
|---|---|---|
| GET | `/items` | Fetch all food items |
| GET | `/items/:id` | Fetch a food item by ID |
| POST | `/items` | Add a new food item |

### GET – Fetch All Items

Request:

`GET http://localhost:3000/items`

Expected status: `200 OK`

### GET – Fetch One Item

Request:

`GET http://localhost:3000/items/1`

Expected status: `200 OK`

If the item does not exist, the API returns `404 Not Found`.

### POST – Add a New Item

Request:

`POST http://localhost:3000/items`

Body (JSON):

```json
{
  "name": "Chole Bhature",
  "price": 80,
  "available": true
}
```

Expected status: `201 Created`.

### POST – Validation

If the required name is missing, the API returns:

`422 Unprocessable Content`

Response:

```json
{
  "error": "name required"
}
```

## 6. HTTP Status Codes

| Status Code | Meaning | Situation |
|---|---|---|
| 200 | OK | GET request successful |
| 201 | Created | New food item added |
| 404 | Not Found | Requested item does not exist |
| 422 | Unprocessable Content | Invalid POST data |

## 7. Postman API Testing

The APIs can be tested using Postman.

Steps:

1. Start the Node.js server.
2. Open Postman.
3. Import `postman/CampusEats-Assignment-8.postman_collection.json`.
4. Select the required API request.
5. Click Send.
6. Check the response and HTTP status code.

The Postman collection includes:

- GET all menu items.
- GET menu item by ID.
- GET invalid ID (404).
- POST new menu item.
- POST missing name (422).
- GET menu after creating a new item.

## 8. Answers to Assignment Questions

### Q1. Which CampusEats service did you pick, and what are its routes?

We selected the **Menu/Catalogue service**.

Its REST API routes are:

- GET `/items` – Fetch all menu items.
- GET `/items/:id` – Fetch a particular menu item.
- POST `/items` – Create a new menu item.

### Q2. Which status codes did you return?

- 200 OK – Successful GET request.
- 201 Created – Successfully created a new menu item.
- 404 Not Found – Requested item ID does not exist.
- 422 Unprocessable Content – Required field is missing or submitted data is invalid.

### Q3. Where did you use req.params and req.body? Why does POST need express.json()?

- `req.params.id` is used to retrieve the item ID from the URL.
- `req.body` is used to access the JSON data submitted by the client.
- `express.json()` parses incoming JSON request bodies and makes the data available through `req.body`.

Without `express.json()`, Express does not automatically parse the incoming JSON body.

## 9. Frontend Functionality

The frontend provides:

- Display of all menu items.
- Food names and prices.
- Availability information.
- A form to add new food items.
- Automatic refresh after successfully adding a new item.

The frontend communicates with the backend using JavaScript Fetch API.

## 10. Project Structure

```text
CS543_A08_CampusEats/
│
├── server.js
├── package.json
├── package-lock.json
├── README.md
├── .gitignore
│
├── public/
│   ├── index.html
│   └── style.css
│
├── postman/
│   └── CampusEats-Assignment-8.postman_collection.json
│
└── professor-starter-original/
    ├── server.js
    ├── package.json
    ├── README.md
    └── public/
        ├── index.html
        └── style.css
```

## 11. Submission Deliverables

- Working REST API with GET and POST routes.
- Frontend HTML and CSS files.
- Postman API testing collection.
- GitHub repository link.
- Before screenshot showing the initial four food items.
- After screenshot showing the newly added food item.
- Demonstration video uploaded to Google Drive.
- Google Drive sharing link submitted through Google Classroom.

**Note:** One submission per team through Google Classroom, as specified in the assignment.

## 12. Conclusion

The CampusEats Menu/Catalogue REST API demonstrates how a frontend application communicates with a backend REST API using HTTP methods and JSON.

Through this assignment, we implemented GET and POST operations, request validation, HTTP status codes, and frontend-backend integration using Node.js and Express.js.
