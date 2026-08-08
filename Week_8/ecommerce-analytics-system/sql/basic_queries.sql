-- ============================================================
-- E-COMMERCE ORDER ANALYTICS SYSTEM
-- BASIC SQL ANALYSIS
-- ============================================================


-- ============================================================
-- 1. TOTAL REVENUE PER CATEGORY
-- ============================================================
-- Revenue = quantity × unit_price ×
--           (1 - discount_percent / 100)

SELECT
    p.category,
    ROUND(
        SUM(
            oi.quantity
            * oi.unit_price
            * (1 - oi.discount_percent / 100.0)
        ),
        2
    ) AS total_revenue
FROM order_items oi
JOIN orders o
    ON oi.order_id = o.order_id
JOIN products p
    ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;


-- ============================================================
-- 2. TOP 10 CUSTOMERS BY TOTAL ORDER VALUE
-- ============================================================

SELECT
    c.customer_id,
    c.customer_name,
    ROUND(
        SUM(
            oi.quantity
            * oi.unit_price
            * (1 - oi.discount_percent / 100.0)
        ),
        2
    ) AS total_order_value
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY
    c.customer_id,
    c.customer_name
ORDER BY total_order_value DESC
LIMIT 10;


-- ============================================================
-- 3. MONTH-WISE ORDER COUNT FOR THE LAST 12 MONTHS
-- ============================================================
-- SQLite date functions are used here.
-- The query calculates the latest order month in the
-- database and returns the 12-month period ending there.

WITH latest_month AS (
    SELECT
        date(
            MAX(order_date),
            'start of month'
        ) AS max_month
    FROM orders
)

SELECT
    strftime('%Y-%m', o.order_date) AS order_month,
    COUNT(*) AS order_count
FROM orders o
CROSS JOIN latest_month lm
WHERE date(o.order_date) >= date(
        lm.max_month,
        '-11 months'
      )
GROUP BY
    strftime('%Y-%m', o.order_date)
ORDER BY order_month;