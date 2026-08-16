# CampusEats Service Contracts

## Task 3 — Service Contracts

Contracts define the operations that other services may call. 
The contract exposes the operation, its input, output, and possible errors.
Internal database tables and implementation details are hidden from callers.

---

## 1. Orders Service

### 1. placeOrder

**Input:**
- studentId
- items: [{itemId, qty}]
- deliveryAddressId
- paymentMethodId

**Output:**
- orderId
- status
- total
- estimatedMinutes

**Errors:**
- empty cart
- item unavailable
- invalid address
- payment declined

### 2. getOrder

**Input:**
- orderId

**Output:**
- orderId
- status
- items
- total
- deliveryAddressId

**Errors:**
- order not found

### 3. cancelOrder

**Input:**
- orderId

**Output:**
- orderId
- status

**Errors:**
- order not found
- order cannot be cancelled

---

## 2. Catalogue Service

### 1. listRestaurants

**Input:**
- area / filter

**Output:**
- restaurants[]

**Errors:**
- none

### 2. getMenu

**Input:**
- restaurantId

**Output:**
- menu[]

**Errors:**
- restaurant not found

### 3. checkItem

**Input:**
- itemId
- quantity

**Output:**
- itemId
- available
- price

**Errors:**
- item not found
- item unavailable

---

## 3. Payments Service

### 1. charge

**Input:**
- orderId
- amount
- paymentMethodId

**Output:**
- transactionId
- status
- receipt

**Errors:**
- payment declined
- invalid payment method

---

## 4. Delivery Service

### 1. assignRider

**Input:**
- orderId
- deliveryAddressId

**Output:**
- assignmentId
- riderId
- status

**Errors:**
- no rider available
- invalid delivery address

---

## 5. Notifications Service

### 1. send

**Input:**
- userId
- message
- channel

**Output:**
- notificationId
- status

**Errors:**
- invalid user
- delivery failed

---

## 6. Accounts Service

### 1. getProfile

**Input:**
- userId

**Output:**
- userId
- name
- email
- addresses

**Errors:**
- user not found