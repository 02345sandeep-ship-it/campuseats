// CS543 Assignment 8 — CampusEats Menu/Catalogue REST API
// Data is intentionally stored in memory, as specified in the assignment.

const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware: parse JSON request bodies and serve the frontend from /public.
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Four initial menu records (source of truth for this assignment).
let items = [
  { id: 1, name: 'Veg Thali', price: 90, available: true },
  { id: 2, name: 'Paneer Roll', price: 70, available: true },
  { id: 3, name: 'Masala Dosa', price: 60, available: true },
  { id: 4, name: 'Veg Biryani', price: 120, available: false }
];
let nextId = 5;

// GET /items — return the complete menu (200 OK).
app.get('/items', (req, res) => {
  return res.status(200).json(items);
});

// GET /items/:id — return one menu item, or 404 when it does not exist.
app.get('/items/:id', (req, res) => {
  const id = Number(req.params.id);
  if (!Number.isInteger(id) || id < 1) {
    return res.status(404).json({ error: 'item not found' });
  }
  const item = items.find((entry) => entry.id === id);
  if (!item) return res.status(404).json({ error: 'item not found' });
  return res.status(200).json(item);
});

// POST /items — validate JSON and create a menu item (201 Created).
app.post('/items', (req, res) => {
  const body = req.body || {};
  const name = typeof body.name === 'string' ? body.name.trim() : '';
  const price = Number(body.price);
  const available = body.available === undefined ? true : body.available;

  // Assignment requirement: 422 when a required field is missing.
  if (!name) return res.status(422).json({ error: 'name required' });
  if (body.price === undefined || body.price === '' || !Number.isFinite(price) || price < 0) {
    return res.status(422).json({ error: 'price must be a non-negative number' });
  }
  if (typeof available !== 'boolean') {
    return res.status(422).json({ error: 'available must be true or false' });
  }

  const newItem = { id: nextId++, name, price, available };
  items.push(newItem);
  return res.status(201).json(newItem);
});

// Return a clear response for malformed JSON sent by a client.
app.use((err, req, res, next) => {
  if (err instanceof SyntaxError && err.status === 400 && 'body' in err) {
    return res.status(400).json({ error: 'invalid JSON body' });
  }
  console.error(err);
  return res.status(500).json({ error: 'internal server error' });
});

app.listen(PORT, () => {
  console.log(`CampusEats Menu API running at http://localhost:${PORT}`);
  console.log('Routes: GET /items | GET /items/:id | POST /items');
});
