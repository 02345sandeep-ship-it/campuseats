CREATE DATABASE IF NOT EXISTS campuseats_graphql
  CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

USE campuseats_graphql;

CREATE TABLE IF NOT EXISTS dishes (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR(120) NOT NULL,
  price DECIMAL(10, 2) NOT NULL,
  available BOOLEAN NOT NULL DEFAULT TRUE,
  PRIMARY KEY (id),
  CONSTRAINT chk_dishes_price_nonnegative CHECK (price >= 0)
);

INSERT INTO dishes (name, price, available)
SELECT seed.name, seed.price, seed.available
FROM (
  SELECT 'Paneer Wrap' AS name, 90.00 AS price, TRUE AS available
  UNION ALL SELECT 'Masala Dosa', 75.00, TRUE
  UNION ALL SELECT 'Veg Biryani', 110.00, TRUE
  UNION ALL SELECT 'Cold Coffee', 55.00, FALSE
) AS seed
WHERE NOT EXISTS (SELECT 1 FROM dishes);
