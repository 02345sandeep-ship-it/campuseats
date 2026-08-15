# CampusEats Brief

## What is CampusEats?

CampusEats is a campus food ordering and delivery system. Students can log in, manage their profile and delivery addresses, browse campus restaurants and their menus, add food items to a cart, place orders, and pay online.

After an order is placed, a rider is assigned to deliver the food. The student can track the delivery. The system also sends notifications as the order moves through different stages such as order placed, paid, on the way, and delivered.

The system can be divided into separate services based on their capabilities and data ownership. The tutorial identifies six services: Accounts, Catalogue, Orders, Payments, Delivery, and Notifications. Each service owns its own data and other services interact with it through published contracts rather than directly accessing its internal tables. :contentReference[oaicite:1]{index=1}

## Who Uses CampusEats?

### 1. Students

Students are the main users of CampusEats. They:

- Log in.
- Manage their profile and delivery addresses.
- Browse restaurants and menus.
- Add items to a cart.
- Place orders.
- Pay online.
- Track their food delivery.
- Receive order-status notifications.

### 2. Riders

Riders are responsible for delivering food to students. A rider is assigned to an order and carries out the delivery. :contentReference[oaicite:2]{index=2}

### 3. Campus Restaurants

Restaurants provide the food available through CampusEats. Their restaurants, menus, and prices are managed by the Catalogue capability/service. :contentReference[oaicite:3]{index=3}

### 4. CampusEats Services

Internally, CampusEats is divided into services that own different parts of the system's data:

- Accounts
- Catalogue
- Orders
- Payments
- Delivery
- Notifications

## Nouns — Things / Services / Data

The important nouns in CampusEats are:

### Users and Accounts

- Students
- Users
- Profiles
- Addresses
- Login

### Catalogue

- Restaurants
- Menus
- Menu items
- Prices

### Orders

- Carts
- Orders
- Order status
- Order items

### Payments

- Transactions
- Refunds
- Payment method
- Receipt

### Delivery

- Riders
- Assignments
- Delivery

### Notifications

- Notifications
- Message log

The tutorial groups these nouns according to data ownership. For example, Accounts owns users, addresses, and login; Catalogue owns restaurants, menus, and prices; Orders owns carts, orders, and status; Payments owns transactions and refunds; Delivery owns riders and assignments; and Notifications owns the message log. :contentReference[oaicite:4]{index=4}

## Verbs — Actions / Tasks / Contracts

The main verbs or actions in CampusEats are:

### Student Actions

- log in
- manage profile
- manage addresses
- browse restaurants
- browse menus
- add to cart
- place order
- pay
- track delivery
- receive notifications

### Service Operations

Important service operations include:

- `addToCart`
- `placeOrder`
- `getOrder`
- `cancelOrder`
- `listRestaurants`
- `getMenu`
- `checkItem`
- `charge`
- `refund`
- `assignRider`
- `send`

The tutorial explains that these operations are the verbs that services offer to the outside world through their contracts. :contentReference[oaicite:5]{index=5}

## Service Boundaries

CampusEats has six main service boundaries:

| Service | Data it owns |
|---|---|
| Accounts | users, addresses, login |
| Catalogue | restaurants, menus, prices |
| Orders | carts, orders, status |
| Payments | transactions, refunds |
| Delivery | riders, assignments |
| Notifications | message log |

Each service owns its own data. Other services should not directly access another service's database tables. Instead, they use the service's published contract. This supports independence and loose coupling. :contentReference[oaicite:6]{index=6}

## Example of Service Interaction

When a student places an order, the services work together:

1. Student calls `Orders.placeOrder`.
2. Orders calls `Catalogue.checkItem` to check availability and price.
3. Orders calls `Payments.charge` to take the payment.
4. Orders calls `Delivery.assignRider` to arrange delivery.
5. Orders calls `Notifications.send` to notify the student.
6. Orders returns the order confirmation to the student.

The Orders service coordinates the process, but it does not directly read the data owned by Catalogue, Payments, or Delivery. It uses their published contracts instead. :contentReference[oaicite:7]{index=7}

## Summary

CampusEats is a campus food ordering and delivery system used mainly by students, with restaurants and riders participating in the process. Its main capabilities cover accounts, food catalogue, ordering, payments, delivery, and notifications.

The important design idea is:

**Capabilities → Data Ownership → Boundaries → Contracts**

Each service has one clear responsibility, owns its own data, and exposes operations through contracts while keeping its internal implementation hidden. :contentReference[oaicite:8]{index=8}