-- =========================================================
-- CampusEats Database Schema
-- Assignment 2 - Task 5
-- =========================================================

-- =========================================================
-- 1. ACCOUNTS SERVICE
-- Owns: users, addresses, login
-- =========================================================

CREATE TABLE users (
    user_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    phone VARCHAR(20)
);

CREATE TABLE addresses (
    address_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    address_line VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20),
    is_default BOOLEAN DEFAULT FALSE,

    CONSTRAINT fk_addresses_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
);

CREATE TABLE login (
    login_id INT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,

    CONSTRAINT fk_login_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
);


-- =========================================================
-- 2. CATALOGUE SERVICE
-- Owns: restaurants, menus, prices
-- =========================================================

CREATE TABLE restaurants (
    restaurant_id INT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    area VARCHAR(100),
    address VARCHAR(255),
    status VARCHAR(30) DEFAULT 'ACTIVE'
);

CREATE TABLE menus (
    menu_id INT PRIMARY KEY,
    restaurant_id INT NOT NULL,
    item_name VARCHAR(150) NOT NULL,
    description VARCHAR(500),
    availability BOOLEAN DEFAULT TRUE,

    CONSTRAINT fk_menus_restaurant
        FOREIGN KEY (restaurant_id)
        REFERENCES restaurants(restaurant_id)
);

CREATE TABLE prices (
    price_id INT PRIMARY KEY,
    menu_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'INR',

    CONSTRAINT fk_prices_menu
        FOREIGN KEY (menu_id)
        REFERENCES menus(menu_id)
);


-- =========================================================
-- 3. ORDERS SERVICE
-- Owns: carts, orders, order status
-- =========================================================

CREATE TABLE carts (
    cart_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    delivery_address_id INT NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    status VARCHAR(30) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE order_status (
    status_id INT PRIMARY KEY,
    order_id INT NOT NULL,
    status VARCHAR(30) NOT NULL,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_order_status_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
);


-- =========================================================
-- 4. PAYMENTS SERVICE
-- Owns: transactions, refunds
-- =========================================================

CREATE TABLE transactions (
    transaction_id INT PRIMARY KEY,
    order_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    status VARCHAR(30) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE refunds (
    refund_id INT PRIMARY KEY,
    transaction_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    reason VARCHAR(255),
    status VARCHAR(30) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_refunds_transaction
        FOREIGN KEY (transaction_id)
        REFERENCES transactions(transaction_id)
);


-- =========================================================
-- 5. DELIVERY SERVICE
-- Owns: riders, assignments
-- =========================================================

CREATE TABLE riders (
    rider_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    status VARCHAR(30) DEFAULT 'AVAILABLE'
);

CREATE TABLE assignments (
    assignment_id INT PRIMARY KEY,
    order_id INT NOT NULL,
    rider_id INT NOT NULL,
    status VARCHAR(30) NOT NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_assignments_rider
        FOREIGN KEY (rider_id)
        REFERENCES riders(rider_id)
);


-- =========================================================
-- 6. NOTIFICATIONS SERVICE
-- Owns: message log
-- =========================================================

CREATE TABLE message_log (
    message_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    message VARCHAR(500) NOT NULL,
    channel VARCHAR(30) NOT NULL,
    status VARCHAR(30) NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);