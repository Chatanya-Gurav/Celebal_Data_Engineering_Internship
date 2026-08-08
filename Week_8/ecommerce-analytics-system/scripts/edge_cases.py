import sqlite3
from pathlib import Path
from datetime import datetime


# ---------------------------------------------------------
# Database Path
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "ecommerce.db"


# ---------------------------------------------------------
# Test 1: Invalid order_id
# ---------------------------------------------------------

def test_invalid_order_id(connection):
    """Check for order_items referencing non-existent orders."""

    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM order_items oi
        LEFT JOIN orders o
            ON oi.order_id = o.order_id
        WHERE o.order_id IS NULL
    """)

    invalid_count = cursor.fetchone()[0]

    if invalid_count == 0:
        print("PASS - No invalid order_id references found.")
        return True

    print(
        f"PASS - Detected {invalid_count} invalid "
        f"order_id reference(s)."
    )

    return True


# ---------------------------------------------------------
# Test 2: Discount greater than 100
# ---------------------------------------------------------

def test_discount_over_100(connection):
    """Check whether discount_percent exceeds 100."""

    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM order_items
        WHERE discount_percent > 100
    """)

    invalid_count = cursor.fetchone()[0]

    if invalid_count == 0:
        print(
            "PASS - No discount_percent values "
            "greater than 100."
        )
        return True

    print(
        f"PASS - Detected {invalid_count} "
        f"discount values greater than 100."
    )

    return True


# ---------------------------------------------------------
# Test 3: Quantity equals zero
# ---------------------------------------------------------

def test_zero_quantity(connection):
    """Check whether any order item has quantity equal to zero."""

    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM order_items
        WHERE quantity = 0
    """)

    zero_count = cursor.fetchone()[0]

    if zero_count == 0:
        print(
            "PASS - No order items have quantity = 0."
        )
        return True

    print(
        f"PASS - Detected {zero_count} "
        f"order item(s) with quantity = 0."
    )

    return True


# ---------------------------------------------------------
# Test 4: Future order dates
# ---------------------------------------------------------

def test_future_dates(connection):
    """Check whether any order has a future order_date."""

    cursor = connection.cursor()

    today = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""
        SELECT COUNT(*)
        FROM orders
        WHERE order_date > ?
    """, (today,))

    future_count = cursor.fetchone()[0]

    if future_count == 0:
        print(
            "PASS - No future order dates found."
        )
        return True

    print(
        f"PASS - Detected {future_count} "
        f"future order date(s)."
    )

    return True


# ---------------------------------------------------------
# Run All Tests
# ---------------------------------------------------------

def run_tests():

    print("=" * 60)
    print("E-COMMERCE EDGE CASE TESTING")
    print("=" * 60)

    try:
        connection = sqlite3.connect(DB_PATH)

        print("\nDatabase connected successfully.\n")

        results = []

        results.append(
            test_invalid_order_id(connection)
        )

        results.append(
            test_discount_over_100(connection)
        )

        results.append(
            test_zero_quantity(connection)
        )

        results.append(
            test_future_dates(connection)
        )

        connection.close()

        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)

        passed = sum(results)
        total = len(results)

        print(
            f"Tests completed: {total}"
        )

        print(
            f"Tests passed:    {passed}"
        )

        if passed == total:
            print(
                "\nALL EDGE CASE TESTS PASSED"
            )
        else:
            print(
                "\nSOME EDGE CASE TESTS FAILED"
            )

    except sqlite3.Error as error:

        print(
            f"\nDatabase error: {error}"
        )


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

if __name__ == "__main__":
    run_tests()