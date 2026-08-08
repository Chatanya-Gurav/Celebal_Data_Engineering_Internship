-- ============================================================
-- E-COMMERCE ORDER ANALYTICS SYSTEM
-- COHORT & RETENTION ANALYSIS
-- ============================================================


-- ============================================================
-- 16. CUSTOMER COHORT ANALYSIS
-- ============================================================
-- Cohort = customer's registration month.
--
-- Month 0 = registration month
-- Month 1 = one month after registration
-- Month 2 = two months after registration
-- Month 3 = three months after registration
--
-- The query calculates:
--   - Number of customers ordering in each month
--   - Retention rate for each month
-- ============================================================


WITH customer_registration AS (

    SELECT
        customer_id,

        DATE(
            registration_date,
            'start of month'
        ) AS cohort_month

    FROM customers
),


customer_orders AS (

    SELECT DISTINCT
        o.customer_id,

        DATE(
            o.order_date,
            'start of month'
        ) AS order_month

    FROM orders o

    WHERE o.customer_id IS NOT NULL
),


cohort_activity AS (

    SELECT
        cr.customer_id,
        cr.cohort_month,
        co.order_month,

        (
            (
                CAST(
                    STRFTIME('%Y', co.order_month)
                    AS INTEGER
                )
                -
                CAST(
                    STRFTIME('%Y', cr.cohort_month)
                    AS INTEGER
                )
            ) * 12
            +
            (
                CAST(
                    STRFTIME('%m', co.order_month)
                    AS INTEGER
                )
                -
                CAST(
                    STRFTIME('%m', cr.cohort_month)
                    AS INTEGER
                )
            )
        ) AS month_number

    FROM customer_registration cr

    JOIN customer_orders co
        ON cr.customer_id = co.customer_id

    WHERE co.order_month >= cr.cohort_month
),


cohort_counts AS (

    SELECT
        cohort_month,

        COUNT(
            DISTINCT CASE
                WHEN month_number = 0
                THEN customer_id
            END
        ) AS month_0,

        COUNT(
            DISTINCT CASE
                WHEN month_number = 1
                THEN customer_id
            END
        ) AS month_1,

        COUNT(
            DISTINCT CASE
                WHEN month_number = 2
                THEN customer_id
            END
        ) AS month_2,

        COUNT(
            DISTINCT CASE
                WHEN month_number = 3
                THEN customer_id
            END
        ) AS month_3

    FROM cohort_activity

    GROUP BY cohort_month
)


SELECT
    cohort_month,

    month_0,
    month_1,
    month_2,
    month_3,

    ROUND(
        100.0 * month_0
        / NULLIF(month_0, 0),
        2
    ) AS retention_month_0_percent,

    ROUND(
        100.0 * month_1
        / NULLIF(month_0, 0),
        2
    ) AS retention_month_1_percent,

    ROUND(
        100.0 * month_2
        / NULLIF(month_0, 0),
        2
    ) AS retention_month_2_percent,

    ROUND(
        100.0 * month_3
        / NULLIF(month_0, 0),
        2
    ) AS retention_month_3_percent

FROM cohort_counts

ORDER BY cohort_month;