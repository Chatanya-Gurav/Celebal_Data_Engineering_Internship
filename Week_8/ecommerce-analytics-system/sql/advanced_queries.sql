-- ============================================================
-- E-COMMERCE ORDER ANALYTICS SYSTEM
-- ADVANCED SQL ANALYSIS
-- ============================================================


-- ============================================================
-- 7. RUNNING TOTAL OF REVENUE PER REGION
-- ============================================================
-- Show:
-- region_code, order_date, daily_revenue, running_total

WITH daily_region_revenue AS (
    SELECT
        o.region_code,
        DATE(o.order_date) AS order_date,

        ROUND(
            SUM(
                oi.quantity
                * oi.unit_price
                * (1 - oi.discount_percent / 100.0)
            ),
            2
        ) AS daily_revenue

    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id

    GROUP BY
        o.region_code,
        DATE(o.order_date)
)

SELECT
    region_code,
    order_date,
    daily_revenue,

    ROUND(
        SUM(daily_revenue) OVER (
            PARTITION BY region_code
            ORDER BY order_date
            ROWS BETWEEN UNBOUNDED PRECEDING
            AND CURRENT ROW
        ),
        2
    ) AS running_total

FROM daily_region_revenue

ORDER BY
    region_code,
    order_date;


-- ============================================================
-- 8. RANK PRODUCTS BY TOTAL REVENUE WITHIN CATEGORY
-- ============================================================
-- Products with the same revenue receive the same rank.

WITH product_revenue AS (
    SELECT
        p.category,
        p.product_id,
        p.product_name,

        ROUND(
            SUM(
                oi.quantity
                * oi.unit_price
                * (1 - oi.discount_percent / 100.0)
            ),
            2
        ) AS total_revenue

    FROM products p
    JOIN order_items oi
        ON p.product_id = oi.product_id

    GROUP BY
        p.category,
        p.product_id,
        p.product_name
)

SELECT
    category,
    product_name,
    total_revenue,

    DENSE_RANK() OVER (
        PARTITION BY category
        ORDER BY total_revenue DESC
    ) AS rank_in_category

FROM product_revenue

ORDER BY
    category,
    rank_in_category,
    product_name;


-- ============================================================
-- 9. CUSTOMER ORDER GAP ANALYSIS
-- ============================================================
-- Calculate days between consecutive orders.
-- Flag customers whose average gap is greater than 30 days
-- as "At Risk".

WITH customer_orders AS (
    SELECT
        customer_id,
        DATE(order_date) AS order_date,

        LAG(
            DATE(order_date)
        ) OVER (
            PARTITION BY customer_id
            ORDER BY DATE(order_date)
        ) AS previous_order_date

    FROM orders

    WHERE customer_id IS NOT NULL
),

order_gaps AS (
    SELECT
        customer_id,
        order_date,
        previous_order_date,

        CASE
            WHEN previous_order_date IS NOT NULL
            THEN CAST(
                JULIANDAY(order_date)
                - JULIANDAY(previous_order_date)
                AS INTEGER
            )
        END AS days_gap

    FROM customer_orders
),

average_gaps AS (
    SELECT
        customer_id,
        AVG(days_gap) AS average_gap

    FROM order_gaps

    WHERE days_gap IS NOT NULL

    GROUP BY customer_id
)

SELECT
    og.customer_id,
    og.order_date,
    og.previous_order_date,
    og.days_gap,

    CASE
        WHEN ag.average_gap > 30
        THEN 'At Risk'
        ELSE 'Active'
    END AS customer_status

FROM order_gaps og

JOIN average_gaps ag
    ON og.customer_id = ag.customer_id

ORDER BY
    og.customer_id,
    og.order_date;


-- ============================================================
-- 10. MULTI-LEVEL CTE CUSTOMER VALUE CATEGORY
-- ============================================================
-- Monthly revenue per customer
-- High   : > 10000
-- Medium : 5000 - 10000
-- Low    : < 5000

WITH monthly_customer_revenue AS (

    SELECT
        o.customer_id,

        STRFTIME(
            '%Y-%m',
            o.order_date
        ) AS order_month,

        SUM(
            oi.quantity
            * oi.unit_price
            * (1 - oi.discount_percent / 100.0)
        ) AS monthly_revenue

    FROM orders o

    JOIN order_items oi
        ON o.order_id = oi.order_id

    WHERE o.customer_id IS NOT NULL

    GROUP BY
        o.customer_id,
        STRFTIME('%Y-%m', o.order_date)
),

customer_categories AS (

    SELECT
        customer_id,
        order_month,
        monthly_revenue,

        CASE
            WHEN monthly_revenue > 10000
                THEN 'High'

            WHEN monthly_revenue >= 5000
                THEN 'Medium'

            ELSE 'Low'
        END AS revenue_category

    FROM monthly_customer_revenue
)

SELECT
    order_month,
    revenue_category,
    COUNT(DISTINCT customer_id) AS customer_count

FROM customer_categories

GROUP BY
    order_month,
    revenue_category

ORDER BY
    order_month,
    revenue_category;


-- ============================================================
-- 11. CUSTOMER LIFETIME VALUE QUARTILES USING NTILE
-- ============================================================
-- Divide customers into four quartiles based on
-- total lifetime value.

WITH customer_lifetime_value AS (

    SELECT
        c.customer_id,
        c.customer_name,

        COALESCE(
            SUM(
                oi.quantity
                * oi.unit_price
                * (1 - oi.discount_percent / 100.0)
            ),
            0
        ) AS total_value

    FROM customers c

    LEFT JOIN orders o
        ON c.customer_id = o.customer_id

    LEFT JOIN order_items oi
        ON o.order_id = oi.order_id

    GROUP BY
        c.customer_id,
        c.customer_name
),

quartiled_customers AS (

    SELECT
        customer_id,
        customer_name,
        ROUND(total_value, 2) AS total_value,

        NTILE(4) OVER (
            ORDER BY total_value DESC
        ) AS quartile

    FROM customer_lifetime_value
)

SELECT
    customer_id,
    customer_name,
    total_value,
    quartile,

    CASE
        WHEN quartile = 1 THEN 'Platinum'
        WHEN quartile = 2 THEN 'Gold'
        WHEN quartile = 3 THEN 'Silver'
        WHEN quartile = 4 THEN 'Bronze'
    END AS quartile_label

FROM quartiled_customers

ORDER BY
    quartile,
    total_value DESC;


-- ============================================================
-- 12. YEAR-OVER-YEAR REVENUE COMPARISON
-- ============================================================
-- Compare each month's revenue with the same month
-- from the previous year.

WITH monthly_revenue AS (

    SELECT
        STRFTIME('%Y', o.order_date) AS year,
        STRFTIME('%m', o.order_date) AS month,

        SUM(
            oi.quantity
            * oi.unit_price
            * (1 - oi.discount_percent / 100.0)
        ) AS revenue

    FROM orders o

    JOIN order_items oi
        ON o.order_id = oi.order_id

    GROUP BY
        STRFTIME('%Y', o.order_date),
        STRFTIME('%m', o.order_date)
),

revenue_with_previous_year AS (

    SELECT
        year,
        month,
        revenue,

        LAG(revenue, 12) OVER (
            ORDER BY year, month
        ) AS prev_year_revenue

    FROM monthly_revenue
)

SELECT
    year,
    month,

    ROUND(revenue, 2) AS revenue,

    ROUND(
        prev_year_revenue,
        2
    ) AS prev_year_revenue,

    CASE
        WHEN prev_year_revenue IS NOT NULL
             AND prev_year_revenue != 0

        THEN ROUND(
            (
                (revenue - prev_year_revenue)
                / prev_year_revenue
            ) * 100,
            2
        )

        ELSE NULL
    END AS yoy_growth_percent

FROM revenue_with_previous_year

ORDER BY
    year,
    month;


-- ============================================================
-- 13. FIRST AND MOST RECENT PURCHASED CATEGORY
-- ============================================================
-- Identify category shift between first and latest purchase.

WITH customer_category_orders AS (

    SELECT
        o.customer_id,
        o.order_date,
        p.category,

        ROW_NUMBER() OVER (
            PARTITION BY o.customer_id
            ORDER BY o.order_date ASC
        ) AS first_purchase_rank,

        ROW_NUMBER() OVER (
            PARTITION BY o.customer_id
            ORDER BY o.order_date DESC
        ) AS latest_purchase_rank

    FROM orders o

    JOIN order_items oi
        ON o.order_id = oi.order_id

    JOIN products p
        ON oi.product_id = p.product_id

    WHERE o.customer_id IS NOT NULL
),

first_categories AS (

    SELECT
        customer_id,
        category AS first_category

    FROM customer_category_orders

    WHERE first_purchase_rank = 1
),

latest_categories AS (

    SELECT
        customer_id,
        category AS latest_category

    FROM customer_category_orders

    WHERE latest_purchase_rank = 1
)

SELECT
    f.customer_id,
    f.first_category,
    l.latest_category,

    CASE
        WHEN f.first_category = l.latest_category
            THEN 'No'
        ELSE 'Yes'
    END AS category_shift

FROM first_categories f

JOIN latest_categories l
    ON f.customer_id = l.customer_id

ORDER BY f.customer_id;


-- ============================================================
-- 14. CUMULATIVE REVENUE DISTRIBUTION
-- ============================================================
-- Show:
-- customer_id
-- revenue
-- cumulative_revenue
-- cumulative_percent

WITH customer_revenue AS (

    SELECT
        c.customer_id,

        COALESCE(
            SUM(
                oi.quantity
                * oi.unit_price
                * (1 - oi.discount_percent / 100.0)
            ),
            0
        ) AS revenue

    FROM customers c

    LEFT JOIN orders o
        ON c.customer_id = o.customer_id

    LEFT JOIN order_items oi
        ON o.order_id = oi.order_id

    GROUP BY c.customer_id
),

revenue_distribution AS (

    SELECT
        customer_id,
        revenue,

        SUM(revenue) OVER (
            ORDER BY revenue DESC
            ROWS BETWEEN UNBOUNDED PRECEDING
            AND CURRENT ROW
        ) AS cumulative_revenue,

        SUM(revenue) OVER () AS total_revenue

    FROM customer_revenue
)

SELECT
    customer_id,

    ROUND(
        revenue,
        2
    ) AS revenue,

    ROUND(
        cumulative_revenue,
        2
    ) AS cumulative_revenue,

    ROUND(
        100.0 * cumulative_revenue
        / NULLIF(total_revenue, 0),
        2
    ) AS cumulative_percent

FROM revenue_distribution

ORDER BY revenue DESC;


-- ============================================================
-- 15. SELF-JOIN WITH WINDOW FUNCTION
-- ============================================================
-- Compare each customer's order with the next order
-- placed by the same customer.

WITH customer_orders AS (

    SELECT
        customer_id,
        order_id,
        DATE(order_date) AS order_date,

        LEAD(
            DATE(order_date)
        ) OVER (
            PARTITION BY customer_id
            ORDER BY DATE(order_date)
        ) AS next_order_date

    FROM orders

    WHERE customer_id IS NOT NULL
)

SELECT
    current_order.customer_id,
    current_order.order_id,
    current_order.order_date,
    next_order.order_date AS next_order_date,

    CASE
        WHEN next_order.order_date IS NOT NULL
        THEN CAST(
            JULIANDAY(next_order.order_date)
            - JULIANDAY(current_order.order_date)
            AS INTEGER
        )
    END AS days_until_next_order

FROM customer_orders current_order

LEFT JOIN customer_orders next_order
    ON current_order.customer_id = next_order.customer_id
    AND current_order.next_order_date = next_order.order_date

ORDER BY
    current_order.customer_id,
    current_order.order_date;