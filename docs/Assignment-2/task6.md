# CampusEats — Service Properties Validation

## Task 6 — Five Properties

The CampusEats services are evaluated against the five required service properties.

---

## 1. Reachable Over a Network

**Status: PASS**

Each CampusEats service is designed as an independently reachable service. Other services communicate with it through its published service operations.

Examples:

- Orders → Catalogue: `checkItem`
- Orders → Payments: `charge`
- Orders → Delivery: `assignRider`
- Orders → Notifications: `send`

This means services can communicate over a network instead of directly calling internal database code.

---

## 2. Self-Contained

**Status: PASS**

Each service owns and manages its own data.

Examples:

- Accounts owns users, addresses, and login.
- Catalogue owns restaurants, menus, and prices.
- Orders owns carts, orders, and order status.
- Payments owns transactions and refunds.
- Delivery owns riders and assignments.
- Notifications owns the message log.

A service does not need to expose its internal database implementation to other services.

---

## 3. Has a Contract

**Status: PASS**

Each service exposes defined operations with:

- Input
- Output
- Error cases

Examples:

- Orders → `placeOrder`, `getOrder`, `cancelOrder`
- Catalogue → `listRestaurants`, `getMenu`, `checkItem`
- Payments → `charge`
- Delivery → `assignRider`
- Notifications → `send`
- Accounts → `getProfile`

The contract defines what a service provides without exposing how the operation is internally implemented.

---

## 4. Independent

**Status: PASS**

Each service has a clearly defined responsibility and owns its own data.

For example:

- Orders is responsible for orders.
- Payments is responsible for payments and refunds.
- Delivery is responsible for riders and assignments.
- Catalogue is responsible for restaurants and menus.

A service can change its internal implementation without requiring other services to know its database or internal code.

---

## 5. Loosely Coupled

**Status: PASS**

Services communicate through published contracts instead of directly accessing another service's internal database.

For example:

Orders calls:

- `Catalogue.checkItem`
- `Payments.charge`
- `Delivery.assignRider`
- `Notifications.send`

Orders does not directly access the Catalogue, Payments, Delivery, or Notifications database tables.

This reduces dependencies between services and allows each service to evolve independently.

---

## Validation Summary

| Service | Reachable | Self-contained | Contract | Independent | Loosely Coupled |
|---|---|---|---|---|---|
| Accounts | PASS | PASS | PASS | PASS | PASS |
| Catalogue | PASS | PASS | PASS | PASS | PASS |
| Orders | PASS | PASS | PASS | PASS | PASS |
| Payments | PASS | PASS | PASS | PASS | PASS |
| Delivery | PASS | PASS | PASS | PASS | PASS |
| Notifications | PASS | PASS | PASS | PASS | PASS |

## Conclusion

The CampusEats service design satisfies the five required service properties. The services have clear responsibilities, own their data, expose contracts, communicate through service operations, and avoid direct access to other services' internal data.