import sqlite3
from pathlib import Path
from datetime import datetime, timedelta


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "ecommerce.db"


# ---------------------------------------------------------
# Database Connection
# ---------------------------------------------------------

def connect_database():
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.row_factory = sqlite3.Row
        return connection

    except sqlite3.Error as error:
        print(f"\nDatabase connection error: {error}")
        return None


# ---------------------------------------------------------
# Input Validation
# ---------------------------------------------------------

def get_report_type():
    valid_types = ["daily", "weekly", "monthly"]

    while True:
        report_type = input(
            "\nEnter report type (daily/weekly/monthly): "
        ).strip().lower()

        if report_type in valid_types:
            return report_type

        print(
            "Invalid report type. "
            "Please choose daily, weekly, or monthly."
        )


def get_date_range():
    while True:
        start_input = input(
            "Enter start date (YYYY-MM-DD): "
        ).strip()

        end_input = input(
            "Enter end date (YYYY-MM-DD): "
        ).strip()

        try:
            start_date = datetime.strptime(
                start_input,
                "%Y-%m-%d"
            ).date()

            end_date = datetime.strptime(
                end_input,
                "%Y-%m-%d"
            ).date()

            if start_date > end_date:
                print(
                    "Start date cannot be after end date."
                )
                continue

            return start_date, end_date

        except ValueError:
            print(
                "Invalid date format. "
                "Use YYYY-MM-DD."
            )


# ---------------------------------------------------------
# Previous Period
# ---------------------------------------------------------

def get_previous_period(start_date, end_date):
    period_length = (
        end_date - start_date
    ).days + 1

    previous_end = start_date - timedelta(days=1)

    previous_start = (
        previous_end
        - timedelta(days=period_length - 1)
    )

    return previous_start, previous_end


# ---------------------------------------------------------
# Main Summary
# ---------------------------------------------------------

def get_summary(
    connection,
    start_date,
    end_date
):
    cursor = connection.cursor()

    query = """
        SELECT
            COUNT(DISTINCT o.order_id) AS total_orders,

            COALESCE(
                SUM(
                    oi.quantity
                    * oi.unit_price
                    * (1 - oi.discount_percent / 100.0)
                ),
                0
            ) AS revenue,

            COUNT(
                DISTINCT o.customer_id
            ) AS unique_customers

        FROM orders o

        JOIN order_items oi
            ON o.order_id = oi.order_id

        WHERE DATE(o.order_date)
              BETWEEN ? AND ?
    """

    cursor.execute(
        query,
        (
            start_date.isoformat(),
            end_date.isoformat()
        )
    )

    return cursor.fetchone()


# ---------------------------------------------------------
# Top 3 Products
# ---------------------------------------------------------

def get_top_products(
    connection,
    start_date,
    end_date
):
    cursor = connection.cursor()

    query = """
        SELECT
            p.product_name,

            SUM(
                oi.quantity
            ) AS quantity_sold,

            ROUND(
                SUM(
                    oi.quantity
                    * oi.unit_price
                    * (1 - oi.discount_percent / 100.0)
                ),
                2
            ) AS revenue

        FROM order_items oi

        JOIN orders o
            ON oi.order_id = o.order_id

        JOIN products p
            ON oi.product_id = p.product_id

        WHERE DATE(o.order_date)
              BETWEEN ? AND ?

        GROUP BY
            p.product_id,
            p.product_name

        ORDER BY revenue DESC

        LIMIT 3
    """

    cursor.execute(
        query,
        (
            start_date.isoformat(),
            end_date.isoformat()
        )
    )

    return cursor.fetchall()


# ---------------------------------------------------------
# Previous Period Comparison
# ---------------------------------------------------------

def get_previous_comparison(
    connection,
    current_start,
    current_end
):
    previous_start, previous_end = get_previous_period(
        current_start,
        current_end
    )

    current = get_summary(
        connection,
        current_start,
        current_end
    )

    previous = get_summary(
        connection,
        previous_start,
        previous_end
    )

    current_revenue = float(
        current["revenue"] or 0
    )

    previous_revenue = float(
        previous["revenue"] or 0
    )

    if previous_revenue == 0:

        revenue_change = None

    else:

        revenue_change = (
            (
                current_revenue
                - previous_revenue
            )
            / previous_revenue
        ) * 100

    return (
        previous_start,
        previous_end,
        previous,
        revenue_change
    )


# ---------------------------------------------------------
# Display Report
# ---------------------------------------------------------

def display_report(
    report_type,
    start_date,
    end_date,
    summary,
    top_products,
    comparison
):
    (
        previous_start,
        previous_end,
        previous,
        revenue_change
    ) = comparison

    print("\n")
    print("=" * 70)
    print("E-COMMERCE ORDER ANALYTICS REPORT")
    print("=" * 70)

    print(f"Report Type : {report_type.upper()}")

    print(
        f"Date Range  : "
        f"{start_date} to {end_date}"
    )

    print("-" * 70)

    print(
        f"Total Orders       : "
        f"{summary['total_orders']}"
    )

    print(
        f"Total Revenue      : "
        f"₹{float(summary['revenue'] or 0):,.2f}"
    )

    print(
        f"Unique Customers   : "
        f"{summary['unique_customers']}"
    )

    print("-" * 70)

    print("TOP 3 PRODUCTS")
    print("-" * 70)

    if not top_products:

        print("No products found for this period.")

    else:

        print(
            f"{'Product':<35}"
            f"{'Quantity':>12}"
            f"{'Revenue':>20}"
        )

        print("-" * 70)

        for product in top_products:

            print(
                f"{product['product_name'][:34]:<35}"
                f"{product['quantity_sold']:>12}"
                f"₹{float(product['revenue']):>18,.2f}"
            )

    print("-" * 70)

    print("PREVIOUS PERIOD COMPARISON")
    print("-" * 70)

    print(
        f"Previous Period : "
        f"{previous_start} to {previous_end}"
    )

    print(
        f"Previous Orders : "
        f"{previous['total_orders']}"
    )

    print(
        f"Previous Revenue: "
        f"₹{float(previous['revenue'] or 0):,.2f}"
    )

    if revenue_change is None:

        print(
            "Revenue Change  : "
            "N/A (previous revenue was zero)"
        )

    else:

        print(
            f"Revenue Change  : "
            f"{revenue_change:+.2f}%"
        )

    print("=" * 70)


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    print("=" * 70)
    print("E-COMMERCE ORDER ANALYTICS SYSTEM")
    print("Command-Line Reporting Tool")
    print("=" * 70)

    connection = connect_database()

    if connection is None:
        return

    try:

        report_type = get_report_type()

        start_date, end_date = get_date_range()

        summary = get_summary(
            connection,
            start_date,
            end_date
        )

        top_products = get_top_products(
            connection,
            start_date,
            end_date
        )

        comparison = get_previous_comparison(
            connection,
            start_date,
            end_date
        )

        display_report(
            report_type,
            start_date,
            end_date,
            summary,
            top_products,
            comparison
        )

    except sqlite3.Error as error:

        print(
            f"\nDatabase error: {error}"
        )

    except Exception as error:

        print(
            f"\nUnexpected error: {error}"
        )

    finally:

        connection.close()

        print(
            "\nDatabase connection closed."
        )


if __name__ == "__main__":
    main()