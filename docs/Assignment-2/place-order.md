# CampusEats — placeOrder

## Task 4 — Full Operation Specification
# CampusEats — placeOrder

## Task 4 — Full Operation Specification

`placeOrder` is the central operation of the CampusEats Orders service. It accepts the student's order details, validates the order, coordinates with other services, and returns an order confirmation.

## 1. Input

The operation accepts:

- `studentId`
- `items: [{itemId, qty}]`
- `deliveryAddressId`
- `paymentMethodId`

### Input Description

| Input | Description |
|---|---|
| `studentId` | Identifies the student placing the order |
| `items` | Food items and quantities requested by the student |
| `deliveryAddressId` | Identifies the delivery address |
| `paymentMethodId` | Identifies the payment method to use |

## 2. Output

On successful completion, the operation returns:

- `orderId`
- `status`
- `total`
- `estimatedMinutes`

### Output Description

| Output | Description |
|---|---|
| `orderId` | Identifies the newly created order |
| `status` | Current status of the order |
| `total` | Total amount for the order |
| `estimatedMinutes` | Estimated delivery time |

## 3. Error Cases

The operation can fail with the following errors:

### Empty Cart

The order cannot be placed when no items are provided.

### Item Unavailable

One or more requested items are unavailable.

### Invalid Address

The supplied delivery address is not valid.

### Payment Declined

The payment cannot be completed using the supplied payment method.

## 4. Internal Details Hidden from Callers

The caller only sees the published `placeOrder` contract. The following implementation details remain hidden:

- How the order is stored internally.
- How order identifiers are generated.
- How the total amount is calculated internally.
- How item availability is checked internally.
- Which payment provider or internal payment mechanism is used.
- How the payment transaction is processed internally.
- How a rider is selected or assigned.
- How the delivery estimate is calculated.
- Which database tables or SQL statements are used.

These details are implementation details of the Orders service and are not part of the public contract.

## 5. Service Interactions

During order placement, the Orders service may call other CampusEats services through their published contracts:

1. `Orders → Catalogue: checkItem`
2. `Orders → Payments: charge`
3. `Orders → Delivery: assignRider`
4. `Orders → Notifications: send`

The caller does not need to know how these services implement their operations.

## 6. Successful Flow

A successful `placeOrder` operation can be summarized as:

Student sends order details  
→ Orders validates the request  
→ Catalogue checks requested items  
→ Payments processes the payment  
→ Delivery assigns a rider  
→ Notifications sends an order notification  
→ Orders returns the order confirmation.

## 7. Contract Summary

**Operation:** `placeOrder`

**Input:**
`studentId, items, deliveryAddressId, paymentMethodId`

**Output:**
`orderId, status, total, estimatedMinutes`

**Possible Errors:**
`empty cart, item unavailable, invalid address, payment declined`

**Hidden:**
Internal storage, identifier generation, payment implementation, rider selection, delivery estimation, database tables, and SQL.