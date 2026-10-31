// CampusEats Catalogue — CS543 Web Services Tutorial 8
// REST API built with Node.js and Express. Data is intentionally in memory,
// matching the professor's tutorial (data resets when the server restarts).

const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Starter data supplied in the professor's tutorial.
let items = [
  { id: 1, name: 'Veg Thali', price: 90 },
  { id: 2, name: 'Paneer Roll', price: 70 },
];
let nextId = 3;

// GET /items — list all dishes
app.get('/items', (req, res) => {
  res.json(items);
});

// GET /items/:id — get one dish
app.get('/items/:id', (req, res) => {
  const id = Number(req.params.id);
  if (!Number.isInteger(id) || id < 1) {
    return res.status(400).json({ error: 'id must be a positive integer' });
  }

  const item = items.find((dish) => dish.id === id);
  if (!item) return res.status(404).json({ error: 'not found' });
  return res.json(item);
});

// POST /items — add a dish (201 Created)
app.post('/items', (req, res) => {
  const name = typeof req.body?.name === 'string' ? req.body.name.trim() : '';
  const rawPrice = req.body?.price;
  const price = rawPrice === '' || rawPrice === undefined ? 0 : Number(rawPrice);

  if (!name) return res.status(422).json({ error: 'name required' });
  if (!Number.isFinite(price) || price < 0) {
    return res.status(422).json({ error: 'price must be a non-negative number' });
  }

  const item = { id: nextId++, name, price };
  items.push(item);
  return res.status(201).json(item);
});

// DELETE /items/:id — optional extension suggested on page 5 of the tutorial
app.delete('/items/:id', (req, res) => {
  const id = Number(req.params.id);
  if (!Number.isInteger(id) || id < 1) {
    return res.status(400).json({ error: 'id must be a positive integer' });
  }

  const index = items.findIndex((dish) => dish.id === id);
  if (index === -1) return res.status(404).json({ error: 'not found' });

  items.splice(index, 1);
  return res.status(204).send();
});

// Invalid JSON or other request parsing errors
app.use((err, req, res, next) => {
  if (err instanceof SyntaxError && err.status === 400 && 'body' in err) {
    return res.status(400).json({ error: 'invalid JSON body' });
  }
  console.error(err);
  return res.status(500).json({ error: 'internal server error' });
});

app.listen(PORT, () => {
  console.log(`CampusEats Catalogue is running at http://localhost:${PORT}`);
  console.log('REST API: GET /items | GET /items/:id | POST /items | DELETE /items/:id');
});
