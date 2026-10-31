CampusEats Menu/Catalogue REST API --- CS543 Assignment 8
Course: CS543 --- Web Services
Assignment: 8 of 12
Selected CampusEats entity: Menu / Catalogue
Technology: Node.js, Express, HTML, CSS, JavaScript Fetch API

This project implements the Assignment 8 requirements: three REST routes
(list, fetch one, create), an in-memory array with four seed records,
POST validation, and a browser page that reads and creates menu records
through the API.
Team Members
  Full name       Roll number
  Sandeep Gupta   20252651045
  Deepankar Bej   20252651018
  Rikam Gouda     20252651040
  Shivam Rajput   20252651052
1. Requirements
- Node.js 18 or newer (Node.js 20 or 22 LTS recommended; Node 24
  should also work).
- npm (installed with Node.js).
- Visual Studio Code.
- Postman Desktop or Postman Web (for API testing).
Check Node and npm in the VS Code terminal:
node -v
npm -v
2. Run the project in VS Code on Windows
1. Download and extract the ZIP.
2. Open VS Code.
3. Select File → Open Folder and choose the project folder (the
   folder containing server.js and package.json).
4. Select Terminal → New Terminal.
5. Confirm the terminal is in the project folder. If needed, use cd
   to enter the extracted project folder.
6. Install dependencies:
   npm install
7. Start the Express server:
   npm start
8. Keep this terminal open. You should see:
   CampusEats Menu API running at http://localhost:3000
   Routes: GET /items | GET /items/:id | POST /items
9. Open the frontend in Chrome or Edge: http://localhost:3000.
10. The page should show four initial dishes. Use the form to add
    another dish; the new dish should appear after the API responds.
Stop the server with Ctrl + C in the terminal. Optional development
mode: npm run dev.
Important: run commands in the correct folder
Run npm install and npm start in the folder that contains this
project's package.json and server.js. Do not run them in the parent
folder or in professor-starter-original.
3. Initial data
The API starts with four records:
ID Name            Price Available

 1 Veg Thali         ₹90 Yes
 2 Paneer Roll       ₹70 Yes
 3 Masala Dosa       ₹60 Yes
 4 Veg Biryani      ₹120 No
The JavaScript array is the source of truth. Data is held in memory
and resets to these four seed records when the server restarts. A
database is not required for this assignment.
4. Required REST API routes
Base URL: http://localhost:3000
  Method            Path              Purpose           Success / error status
  GET               /items          List all menu     200 OK
items             

  GET               /items/:id      Fetch one item    200 OK, 404 Not Found
using its ID      
POST              /items          Create a menu     201 Created,
item              422 Unprocessable Content
GET all items
Request:
GET http://localhost:3000/items
Expected: 200 OK and a JSON array containing the four seed records.
GET one item
Request:
GET http://localhost:3000/items/1
Expected: 200 OK and the Veg Thali object. Try /items/999 to verify
404 Not Found.
POST a new item
Request:
POST http://localhost:3000/items
Content-Type: application/json
Body (raw JSON):
{
  "name": "Chole Bhature",
  "price": 80,
  "available": true
}
Expected: 201 Created and the newly created item, including its
generated ID.
Verify 422 validation
Send a POST request with this body:
{
  "price": 80,
  "available": true
}
Expected: 422 Unprocessable Content with:
{
  "error": "name required"
}
The API also returns 422 when the price is missing, negative, or not a
valid number.
5. Test APIs using Postman --- step by step
1. Start the server in VS Code with npm start; do not close that
   terminal.
2. Open Postman.
3. Click Import (top-left) → Files.
4. Select postman/CampusEats-Assignment-8.postman_collection.json
   from this project folder.
5. Open the imported CampusEats Assignment 8 API collection.
6. Run the requests one by one using Send. The collection includes
   basic test scripts for expected status codes.
Requests included:

  Request in collection              Method   URL            Expected
  1. List all menu items            GET      /items       200
2. Get item by ID 1               GET      /items/1     200
3. Get missing item (404 check)   GET      /items/999   404
4. Create menu item               POST     /items       201
5. Missing name (422 check)       POST     /items       422
6. List menu after create         GET      /items       200; new item visible

For the POST requests, select Body → raw → JSON if you create a
request manually. Ensure the request header is
Content-Type: application/json.
Postman expected response examples
Successful create --- 201:
{
  "id": 5,
  "name": "Chole Bhature",
  "price": 80,
  "available": true
}
Missing name --- 422:
{ "error": "name required" }
Unknown ID --- 404:
{ "error": "item not found" }
6. How the frontend works
- express.static('public') (configured with an absolute project
  path) serves public/index.html and public/style.css.
- When the page loads, JavaScript calls fetch('/items') to read and
  display the menu.
- The Add a new dish form sends a JSON request using
  fetch('/items', { method: 'POST', ... }).
- After a successful POST, the page calls GET /items again to
  refresh the displayed list.
- Since the page and API use the same Express server and origin, no
  CORS setup is needed.
7. Answers to the assignment README questions
Q1. Which CampusEats service did you pick, and what are its routes (method + path)?
We selected the Menu/Catalogue service. Its routes are:
- GET /items --- list all menu items.
- GET /items/:id --- fetch one menu item by its ID.
- POST /items --- create a new menu item.
Q2. Which status codes did you return, and for which outcomes (200 / 201 / 404 / 422)?
- 200 OK --- the GET request succeeded and the requested list or
  item was returned.
- 201 Created --- a new menu item was successfully created by POST.
- 404 Not Found --- the requested item ID does not exist.
- 422 Unprocessable Content --- the POST body is not valid for
  creating an item, such as when the required name is missing or the
  price is invalid.
Q3. Where did you use req.params and where req.body? Why does POST need express.json()?
- req.params.id is used in GET /items/:id to read the item ID from
  the URL path.
- req.body is used in POST /items to read the submitted name,
  price, and available values.
- express.json() is middleware that parses an incoming JSON request
  body and makes the parsed data available in req.body. Without it,
  Express would not automatically parse the JSON body sent by the
  frontend or Postman.
8. Submission deliverables
Before submitting through Google Classroom, complete this checklist:
- [ ] Confirm the team members' names and roll numbers listed above.
- [ ] Push the project folder to the team's GitHub repository.
- [ ] Run the application and capture a before screenshot showing
  the four initial records.
- [ ] Add one new record live and capture an after screenshot
  showing the new record.
- [ ] Record a short demonstration video showing the app running and
  the API request/response.
- [ ] Upload the video and both screenshots to Google Drive.
- [ ] Set Google Drive link access so the instructor can view the
  files.
- [ ] Submit the GitHub repository link and Google Drive link through
  Google Classroom (one submission per team).
Suggested video flow: show the VS Code project and npm start; open the
webpage; show GET /items and GET /items/1 in Postman; add a new item
through the webpage or Postman; show the 201 response and refreshed
list; show the before/after screenshots.
9. Project structure
CS543_A08_CampusEats/
├── server.js
├── package.json
├── package-lock.json          # generated by npm install
├── .gitignore
├── README.md
├── public/
│   ├── index.html
│   └── style.css
├── postman/
│   └── CampusEats-Assignment-8.postman_collection.json
└── professor-starter-original/
    ├── server.js
    ├── package.json
    ├── README.md
    └── public/
        ├── index.html
        └── style.css
