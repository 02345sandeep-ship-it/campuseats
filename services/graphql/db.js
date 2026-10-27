const mysql = require('mysql2/promise');

function createPool(config = process.env) {
  return mysql.createPool({
    host: config.DB_HOST || '127.0.0.1',
    port: Number(config.DB_PORT || 3306),
    user: config.DB_USER || 'campuseats',
    password: config.DB_PASSWORD || '',
    database: config.DB_NAME || 'campuseats_graphql',
    waitForConnections: true,
    connectionLimit: 5,
    queueLimit: 0,
    decimalNumbers: true,
  });
}

const pool = createPool();

async function verifyDatabase() {
  await pool.query('SELECT id, name, price, available FROM dishes LIMIT 0');
}

async function listDishes() {
  const [rows] = await pool.execute(
    'SELECT id, name, price, available FROM dishes ORDER BY id'
  );
  return rows;
}

async function getDish(id) {
  const [rows] = await pool.execute(
    'SELECT id, name, price, available FROM dishes WHERE id = ?', [id]
  );
  return rows[0] || null;
}

async function insertDish({ name, price }) {
  const [result] = await pool.execute(
    'INSERT INTO dishes (name, price, available) VALUES (?, ?, TRUE)',
    [name, price]
  );
  return getDish(result.insertId);
}

async function closePool() {
  await pool.end();
}

module.exports = { pool, verifyDatabase, listDishes, getDish, insertDish, closePool };
