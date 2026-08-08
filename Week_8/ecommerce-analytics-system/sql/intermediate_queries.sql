-- ============================================================
-- E-COMMERCE ORDER ANALYTICS SYSTEM
-- INTERMEDIATE SQL ANALYSIS
-- ============================================================


-- ============================================================
-- 4. CUSTOMERS WHO PLACED ORDERS BUT NEVER HAD
--    ANY ITEM DELIVERED
-- ============================================================

SELECT
    c.customer_id,
    c.customer_name
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
WHERE NOT EXISTS (
    SELECT 1
    FROM orders delivered_orders
    JOIN order_items oi
        ON delivered_orders.order_id = oi.order_id
    WHERE delivered_orders.customer_id = c.customer_id
      AND delivered_orders.status = 'DELIVERED'
)
GROUP BY
    c.customer_id,
    c.customer_name
ORDER BY c.customer_id;


-- ============================================================
-- 5. PRODUCTS THAT WERE ORDERED BUT HAD MORE RETURNS
--    THAN PURCHASES
-- ============================================================
-- Negative quantity represents a return.
-- Positive quantity represents a purchase.

WITH product_transactions AS (
    SELECT
        p.product_id,
        p.product_name,

        SUM(
            CASE
                WHEN oi.quantity > 0
                THEN oi.quantity
                ELSE 0
            END
        ) AS purchased_quantity,

        SUM(
            CASE
                WHEN oi.quantity < 0
                THEN ABS(oi.quantity)
                ELSE 0
            END
        ) AS returned_quantity

    FROM products p
    JOIN order_items oi
        ON p.product_id = oi.product_id

    GROUP BY
        p.product_id,
        p.product_name
)

SELECT
    product_id,
    product_name,
    purchased_quantity,
    returned_quantity
FROM product_transactions
WHERE returned_quantity > purchased_quantity
ORDER BY returned_quantity DESC;


-- ============================================================
-- 6. RETURN RATE PER CATEGORY
-- ============================================================
-- Return rate = returned items / total items × 100

SELECT
    p.category,

    SUM(
        CASE
            WHEN oi.quantity < 0
            THEN ABS(oi.quantity)
            ELSE 0
        END
    ) AS returned_items,

    SUM(
        ABS(oi.quantity)
    ) AS total_items,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN oi.quantity < 0
                THEN ABS(oi.quantity)
                ELSE 0
            END
        )
        / NULLIF(
            SUM(ABS(oi.quantity)),
            0
        ),
        2
    ) AS return_rate_percent

FROM products p
JOIN order_items oi
    ON p.product_id = oi.product_id

GROUP BY p.category
ORDER BY return_rate_percent DESC;