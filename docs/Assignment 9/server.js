// CS543 Assignment 9 — CampusEats secured Menu/Catalogue REST API
// Assignment 8's in-memory catalogue is retained. Authentication runs before authorization.

require('dotenv').config();

const express = require('express');
const path = require('path');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

const app = express();
const PORT = process.env.PORT || 3000;
const SECRET = process.env.JWT_SECRET;

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Assignment 9: keep the JWT secret in the environment, not in source code.
if (!SECRET) {
  console.error('Missing JWT_SECRET. Create .env from .env.example and set JWT_SECRET.');
  process.exit(1);
}

// Two demo users with different roles. Passwords are stored only as bcrypt hashes.
const users = [
  { id: 1, username: 'customer', role: 'customer', passwordHash: bcrypt.hashSync('customer123', 10) },
  { id: 2, username: 'restaurant', role: 'restaurant', passwordHash: bcrypt.hashSync('restaurant123', 10) }
];

// Assignment 8 catalogue data is unchanged.
let items = [
  { id: 1, name: 'Veg Thali', price: 90, available: true },
  { id: 2, name: 'Paneer Roll', price: 70, available: true },
  { id: 3, name: 'Masala Dosa', price: 60, available: true },
  { id: 4, name: 'Veg Biryani', price: 120, available: false }
];
let nextId = 5;

// POST /login — verify credentials and issue a JWT containing user id and role.
app.post('/login', (req, res) => {
  const { username, password } = req.body || {};
  const user = users.find((entry) => entry.username === username);

  if (!user || typeof password !== 'string' || !bcrypt.compareSync(password, user.passwordHash)) {
    return res.status(401).json({ error: 'invalid username or password' });
  }

  const token = jwt.sign(
    { userId: user.id, role: user.role },
    SECRET,
    { expiresIn: '1h' }
  );

  return res.status(200).json({
    token,
    tokenType: 'Bearer',
    expiresIn: '1h',
    user: { id: user.id, username: user.username, role: user.role }
  });
});

// Authentication: identify the caller from Authorization: Bearer <token>.
function auth(req, res, next) {
  const token = (req.get('Authorization') || '').split(' ')[1];
  try {
    if (!token) throw new Error('missing token');
    req.user = jwt.verify(token, SECRET);
    next();
  } catch {
    return res.status(401).json({ error: 'invalid token' });
  }
}

// Authorization: authentication must run first, so req.user is available.
const requireRole = (...ok) => (req, res, next) =>
  ok.includes(req.user.role) ? next() : res.status(403).json({ error: 'forbidden' });

// Protected read routes: any valid logged-in user can read the catalogue.
app.get('/items', auth, (req, res) => {
  return res.status(200).json(items);
});

app.get('/items/:id', auth, (req, res) => {
  const id = Number(req.params.id);
  if (!Number.isInteger(id) || id < 1) {
    return res.status(404).json({ error: 'item not found' });
  }
  const item = items.find((entry) => entry.id === id);
  if (!item) return res.status(404).json({ error: 'item not found' });
  return res.status(200).json(item);
});

// Protected write route: only restaurant/admin may create catalogue items.
app.post('/items', auth, requireRole('restaurant', 'admin'), (req, res) => {
  const body = req.body || {};
  const name = typeof body.name === 'string' ? body.name.trim() : '';
  const price = Number(body.price);
  const available = body.available === undefined ? true : body.available;

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

// Handle malformed JSON requests.
app.use((err, req, res, next) => {
  if (err instanceof SyntaxError && err.status === 400 && 'body' in err) {
    return res.status(400).json({ error: 'invalid JSON body' });
  }
  console.error(err);
  return res.status(500).json({ error: 'internal server error' });
});

app.listen(PORT, () => {
  console.log(`CampusEats Secured API running at http://localhost:${PORT}`);
  console.log('Routes: POST /login | GET /items | GET /items/:id | POST /items');
});
