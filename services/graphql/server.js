const { readFile } = require('node:fs/promises');
const path = require('node:path');
require('dotenv').config({ path: path.join(__dirname, '.env') });
const { ApolloServer } = require('@apollo/server');
const { GraphQLError } = require('graphql');
const express = require('express');
const cors = require('cors');
const { expressMiddleware } = require('@as-integrations/express4');
const db = require('./db');

const typeDefs = readFile(path.join(__dirname, 'schema.graphql'), 'utf8');

function validateDishInput(input) {
  if (typeof input.name !== 'string' || !input.name.trim()) {
    throw new Error('Dish name must not be empty.');
  }
  if (input.name.trim().length > 120) {
    throw new Error('Dish name must be 120 characters or fewer.');
  }
  if (typeof input.price !== 'number' || !Number.isFinite(input.price) || input.price < 0) {
    throw new Error('Dish price must be a non-negative number.');
  }
}

async function databaseRequest(operation) {
  try {
    return await operation();
  } catch (error) {
    console.error('GraphQL database operation failed:', error.message);
    throw new GraphQLError('The menu database is unavailable. Please try again later.', {
      extensions: { code: 'INTERNAL_SERVER_ERROR' },
    });
  }
}

const resolvers = {
  Query: {
    dishes: () => databaseRequest(() => db.listDishes()),
    dish: (_parent, { id }) => databaseRequest(() => db.getDish(id)),
  },
  Mutation: {
    addDish: (_parent, { input }) => {
      validateDishInput(input);
      return databaseRequest(() => db.insertDish({ name: input.name.trim(), price: input.price }));
    },
  },
};

async function start() {
  try {
    await db.verifyDatabase();
  } catch (error) {
    const nextStep = error.code === 'ER_NO_SUCH_TABLE'
      ? 'Run npm run db:init.'
      : 'Check services/graphql/.env and MySQL.';
    throw new Error(`MySQL verification failed for ${process.env.DB_HOST || '127.0.0.1'}:${process.env.DB_PORT || 3306}/${process.env.DB_NAME || 'campuseats_graphql'} (${error.code || 'database error'}). ${nextStep}`);
  }

  const server = new ApolloServer({
    typeDefs: await typeDefs,
    resolvers,
    introspection: process.env.NODE_ENV !== 'production',
  });
  await server.start();
  const app = express();
  app.use(express.static(path.join(__dirname, 'public')));
  app.use('/graphql', cors(), express.json(), expressMiddleware(server));
  const port = Number(process.env.PORT || 4000);
  const httpServer = await new Promise((resolve, reject) => {
    const listener = app.listen(port, '0.0.0.0', () => resolve(listener));
    listener.once('error', reject);
  });
  console.log('CampusEats GraphQL is connected to MySQL.');
  console.log(`Frontend: http://localhost:${port}/`);
  console.log(`GraphQL:  http://localhost:${port}/graphql`);
  return {
    server,
    httpServer,
    url: `http://localhost:${port}/graphql`,
    async stop() {
      await new Promise((resolve, reject) => httpServer.close((error) => error ? reject(error) : resolve()));
      await server.stop();
      await db.closePool();
    },
  };
}

if (require.main === module) {
  let running;
  start().then((instance) => { running = instance; }).catch(async (error) => {
    console.error('Could not start GraphQL service. Check MySQL and services/graphql/.env.', error.message);
    await db.closePool().catch(() => {});
    process.exitCode = 1;
  });

  const shutdown = async () => {
    if (running) await running.stop();
  };
  process.once('SIGINT', shutdown);
  process.once('SIGTERM', shutdown);
}

module.exports = { resolvers, validateDishInput, start };
