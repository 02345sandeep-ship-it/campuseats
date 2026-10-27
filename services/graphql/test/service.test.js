const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const { buildSchema, graphql } = require('graphql');
const { resolvers, validateDishInput } = require('../server');

test('GraphQL schema parses and exposes required fields and operations', async () => {
  const schema = buildSchema(fs.readFileSync(require.resolve('../schema.graphql'), 'utf8'));
  assert.ok(schema.getType('Dish'));
  assert.match(String(schema.getType('Dish').getFields().id.type), /!/);
  assert.ok(schema.getQueryType().getFields().dishes);
  assert.ok(schema.getMutationType().getFields().addDish);
});

test('dish input validation rejects empty names and invalid prices', () => {
  assert.throws(() => validateDishInput({ name: ' ', price: 10 }), /name/);
  assert.throws(() => validateDishInput({ name: 'Soup', price: -1 }), /price/);
  assert.throws(() => validateDishInput({ name: 'Soup', price: NaN }), /price/);
  assert.doesNotThrow(() => validateDishInput({ name: ' Soup ', price: 0 }));
});

test('resolver operations use the SQL data layer', async (t) => {
  if (process.env.RUN_DB_INTEGRATION !== '1' || process.env.DB_NAME !== 'campuseats_graphql_test') {
    t.skip('Set RUN_DB_INTEGRATION=1 and DB_NAME=campuseats_graphql_test to enable isolated MySQL integration checks.');
    return;
  }
  const db = require('../db');
  const name = `GraphQL test ${Date.now()}`;
  try {
    const added = await resolvers.Mutation.addDish(null, { input: { name, price: 12.5 } });
    assert.equal(added.name, name);
    assert.equal(added.available, 1);
    assert.equal((await resolvers.Query.dish(null, { id: added.id })).name, name);
    assert.ok((await resolvers.Query.dishes()).some((dish) => dish.id === added.id));
    assert.equal(await resolvers.Query.dish(null, { id: 4294967295 }), null);
  } finally {
    await db.pool.execute('DELETE FROM dishes WHERE name = ?', [name]);
    await db.closePool();
  }
});

test('database failure is surfaced as a GraphQL error', async (t) => {
  if (process.env.RUN_DB_INTEGRATION !== '1' || process.env.DB_NAME !== 'campuseats_graphql_test') {
    t.skip('Set RUN_DB_INTEGRATION=1 and DB_NAME=campuseats_graphql_test to enable database failure check.');
    return;
  }
  // A separate unreachable port avoids mutating the configured application database.
  const originalPort = process.env.DB_PORT;
  process.env.DB_PORT = '1';
  const dbPath = require.resolve('../db');
  delete require.cache[dbPath];
  const db = require('../db');
  const schema = buildSchema(fs.readFileSync(require.resolve('../schema.graphql'), 'utf8'));
  try {
    const result = await graphql({
      schema,
      source: '{ dishes { id } }',
      rootValue: { dishes: () => db.listDishes() },
    });
    assert.ok(result.errors?.length);
  } finally {
    await db.closePool().catch(() => {});
    delete require.cache[dbPath];
    if (originalPort === undefined) delete process.env.DB_PORT;
    else process.env.DB_PORT = originalPort;
  }
});
