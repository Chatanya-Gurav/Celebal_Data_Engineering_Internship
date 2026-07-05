/* Week 3 Assignment
   Name: Chaitanya Gurav
   Topic: Subqueries, CTEs and Window Functions
*/
-- ------------------------------
-- ----- Step 1: Setup Data -----
-- ------------------------------

-- Create database
CREATE DATABASE week3;

-- ----------------------------

-- Use database
USE week3;

-- ----------------------------

-- Check imported data
SELECT *
FROM superstore_raw
LIMIT 10;

-- ----------------------------

-- Check table structure
DESCRIBE superstore_raw;

-- ----------------------------

-- Count total records
SELECT COUNT(*) AS Total_Rows
FROM superstore_raw;

-- ----------------------------

-- Create customers table
CREATE TABLE customers (
    customer_id VARCHAR(20),
    customer_name VARCHAR(100),
    segment VARCHAR(50),
    country VARCHAR(50),
    city VARCHAR(50),
    state VARCHAR(50),
    postal_code INT,
    region VARCHAR(50)
);

-- ----------------------------

-- Create orders table
CREATE TABLE orders (
    order_id VARCHAR(20),
    order_date DATE,
    ship_date DATE,
    ship_mode VARCHAR(50),
    customer_id VARCHAR(20),
    product_id VARCHAR(20),
    sales DECIMAL(10,2),
    quantity INT,
    discount DECIMAL(5,2),
    profit DECIMAL(10,2)
);

-- ----------------------------

-- Create products table
CREATE TABLE products (
    product_id VARCHAR(20),
    category VARCHAR(50),
    sub_category VARCHAR(50),
    product_name VARCHAR(255)
);

-- ----------------------------

-- Insert data into customers table
INSERT INTO customers
SELECT DISTINCT
    `Customer ID`,
    `Customer Name`,
    Segment,
    Country,
    City,
    State,
    `Postal Code`,
    Region
FROM superstore_raw;

-- ----------------------------

-- Insert data into orders table
INSERT INTO orders
SELECT DISTINCT
    `Order ID`,
    STR_TO_DATE(`Order Date`, '%d-%m-%Y'),
    STR_TO_DATE(`Ship Date`, '%d-%m-%Y'),
    `Ship Mode`,
    `Customer ID`,
    `Product ID`,
    Sales,
    Quantity,
    Discount,
    Profit
FROM superstore_raw;

-- ----------------------------

-- Insert data into products table
INSERT INTO products
SELECT DISTINCT
    `Product ID`,
    Category,
    `Sub-Category`,
    `Product Name`
FROM superstore_raw;

-- ----------------------------

-- Check records in customers table
SELECT COUNT(*) AS Total_Customers
FROM customers;

-- ----------------------------

-- Check records in orders table
SELECT COUNT(*) AS Total_Orders
FROM orders;

-- ----------------------------

-- Check records in products table
SELECT COUNT(*) AS Total_Products
FROM products;

-- --------------------------------------------
-- ----- Step 2: Perform Required Queries -----
-- --------------------------------------------

-- Query 1
-- Find all orders where sales are greater than the average sales. (Subquery)  

SELECT *
FROM orders
WHERE sales > (
    SELECT AVG(sales)
    FROM orders
);

-- ----------------------------

-- Query 2
-- Find the highest sales order for each customer. (Subquery)  

SELECT *
FROM orders o
WHERE sales = (
    SELECT MAX(sales)
    FROM orders
    WHERE customer_id = o.customer_id
);

-- ----------------------------

-- Query 3
-- Calculate total sales for each customer. (CTE)  

WITH customer_sales AS (
    SELECT customer_id,
           SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)
SELECT *
FROM customer_sales;

-- ----------------------------

-- Query 4
-- Find customers whose total sales are above average. (CTE + Subquery)  

WITH customer_sales AS (
    SELECT customer_id,
           SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)
SELECT *
FROM customer_sales
WHERE total_sales >
(
    SELECT AVG(total_sales)
    FROM customer_sales
);

-- ----------------------------

-- Query 5
-- Rank all customers based on total sales. (Window Function)  

WITH customer_sales AS (
    SELECT customer_id,
           SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)
SELECT customer_id,
       total_sales,
       RANK() OVER(ORDER BY total_sales DESC) AS customer_rank
FROM customer_sales;

-- ----------------------------

-- Query 6
-- Assign row numbers to each order within a customer. (Window Function + PARTITION BY)  

SELECT order_id,
       customer_id,
       sales,
       ROW_NUMBER() OVER(PARTITION BY customer_id ORDER BY sales DESC) AS row_num
FROM orders;

-- ----------------------------

-- Query 7
-- Display top 3 customers based on total sales. (Window Function)  

WITH customer_sales AS (
    SELECT customer_id,
           SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)
SELECT *
FROM
(
    SELECT customer_id,
           total_sales,
           RANK() OVER(ORDER BY total_sales DESC) AS customer_rank
    FROM customer_sales
) t
WHERE customer_rank <= 3;

-- ----------------------------

-- -----------------------------------------
-- ----- Step 3: Final Combined Query  -----
-- -----------------------------------------

-- Write one final query that shows: 
-- --Customer Name  
-- --Total Sales  
-- --Rank  
-- --(Use JOIN + CTE + Window Function together) 

WITH customer_sales AS (
    SELECT customer_id,
           SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)

SELECT c.customer_name,
       cs.total_sales,
       RANK() OVER(ORDER BY cs.total_sales DESC) AS customer_rank
FROM customer_sales cs
JOIN customers c
ON cs.customer_id = c.customer_id;

-- ----------------------------

-- --------------------------------------------------
-- ----- Mini Project: Customer Sales Insights  -----
-- --------------------------------------------------

-- Who are the top 5 customers? 

WITH customer_sales AS (
    SELECT customer_id,
           SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)

SELECT c.customer_name,
       total_sales
FROM customer_sales cs
JOIN customers c
ON cs.customer_id = c.customer_id
ORDER BY total_sales DESC
LIMIT 5;

-- ----------------------------

-- Who are the bottom 5 customers?  

WITH customer_sales AS (
    SELECT customer_id,
           SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)

SELECT c.customer_name,
       total_sales
FROM customer_sales cs
JOIN customers c
ON cs.customer_id = c.customer_id
ORDER BY total_sales
LIMIT 5;

-- ----------------------------

-- Which customers made only one order?  

SELECT c.customer_name,
       COUNT(o.order_id) AS total_orders
FROM customers c
JOIN orders o
ON c.customer_id = o.customer_id
GROUP BY c.customer_name
HAVING COUNT(o.order_id) = 1;

-- -->There are no customers in this Superstore dataset who placed exactly one order.

-- --> We can Use COUNT(DISTINCT order_id) instead:
SELECT c.customer_name,
       COUNT(DISTINCT o.order_id) AS total_orders
FROM customers c
JOIN orders o
ON c.customer_id = o.customer_id
GROUP BY c.customer_name
HAVING COUNT(DISTINCT o.order_id) = 1;

-- ----------------------------

-- Which customers have above-average sales?  

WITH customer_sales AS (
    SELECT customer_id,
           SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)

SELECT c.customer_name,
       total_sales
FROM customer_sales cs
JOIN customers c
ON cs.customer_id = c.customer_id
WHERE total_sales >
(
    SELECT AVG(total_sales)
    FROM customer_sales
);

-- ----------------------------

-- What is the highest order value per customer? 

SELECT c.customer_name,
       MAX(o.sales) AS highest_order_value
FROM customers c
JOIN orders o
ON c.customer_id = o.customer_id
GROUP BY c.customer_name;

