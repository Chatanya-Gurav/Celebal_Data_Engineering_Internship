-- ============================================================
-- E-COMMERCE ORDER ANALYTICS SYSTEM
-- Database Schema
-- ============================================================

-- Enable foreign key enforcement
PRAGMA foreign_keys = ON;


-- ============================================================
-- 1. CUSTOMERS TABLE
-- ============================================================

DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;


CREATE TABLE customers (
    customer_id TEXT PRIMARY KEY,
    customer_name TEXT NOT NULL,
    email TEXT,
    registration_date TEXT,
    customer_type TEXT NOT NULL
);


-- ============================================================
-- 2. PRODUCTS TABLE
-- ============================================================

CREATE TABLE products (
    product_id TEXT PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    subcategory TEXT,
    cost_price REAL NOT NULL
);


-- ============================================================
-- 3. ORDERS TABLE
-- ============================================================

CREATE TABLE orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT,
    order_date TEXT NOT NULL,
    status TEXT NOT NULL,
    region_code TEXT NOT NULL,

    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);


-- ============================================================
-- 4. ORDER ITEMS TABLE
-- ============================================================

CREATE TABLE order_items (
    item_id TEXT PRIMARY KEY,
    order_id TEXT NOT NULL,
    product_id TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    discount_percent REAL NOT NULL,

    FOREIGN KEY (order_id)
        REFERENCES orders(order_id),

    FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);


-- ============================================================
-- VERIFICATION QUERIES
-- ============================================================

-- Show all tables
SELECT name
FROM sqlite_master
WHERE type = 'table'
ORDER BY name;


-- Check table row counts
SELECT 'customers' AS table_name, COUNT(*) AS row_count
FROM customers

UNION ALL

SELECT 'products', COUNT(*)
FROM products

UNION ALL

SELECT 'orders', COUNT(*)
FROM orders

UNION ALL

SELECT 'order_items', COUNT(*)
FROM order_items;