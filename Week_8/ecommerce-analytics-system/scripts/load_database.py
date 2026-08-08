import sqlite3
from pathlib import Path
import pandas as pd


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

CLEAN_DIR = BASE_DIR / "data" / "cleaned"
DATABASE_DIR = BASE_DIR / "database"

DATABASE_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DATABASE_DIR / "ecommerce.db"


# ---------------------------------------------------------
# Database Connection
# ---------------------------------------------------------

def create_connection():
    """Create SQLite database connection."""
    try:
        connection = sqlite3.connect(DB_PATH)
        print(f"Connected to database: {DB_PATH}")
        return connection

    except sqlite3.Error as error:
        print(f"Database connection error: {error}")
        return None


# ---------------------------------------------------------
# Create Database Tables
# ---------------------------------------------------------

def create_tables(connection):
    """Create tables with primary and foreign key constraints."""

    cursor = connection.cursor()

    # Enable foreign key enforcement in SQLite
    cursor.execute("PRAGMA foreign_keys = ON")

    # Drop existing tables so the script can be safely re-run
    cursor.execute("DROP TABLE IF EXISTS order_items")
    cursor.execute("DROP TABLE IF EXISTS orders")
    cursor.execute("DROP TABLE IF EXISTS products")
    cursor.execute("DROP TABLE IF EXISTS customers")

    # Customers table
    cursor.execute("""
        CREATE TABLE customers (
            customer_id TEXT PRIMARY KEY,
            customer_name TEXT NOT NULL,
            email TEXT,
            registration_date TEXT,
            customer_type TEXT NOT NULL
        )
    """)

    # Products table
    cursor.execute("""
        CREATE TABLE products (
            product_id TEXT PRIMARY KEY,
            product_name TEXT NOT NULL,
            category TEXT NOT NULL,
            subcategory TEXT,
            cost_price REAL NOT NULL
        )
    """)

    # Orders table
    cursor.execute("""
        CREATE TABLE orders (
            order_id TEXT PRIMARY KEY,
            customer_id TEXT,
            order_date TEXT NOT NULL,
            status TEXT NOT NULL,
            region_code TEXT NOT NULL,

            FOREIGN KEY (customer_id)
                REFERENCES customers(customer_id)
        )
    """)

    # Order Items table
    cursor.execute("""
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
        )
    """)

    connection.commit()

    print("Database tables created successfully.")


# ---------------------------------------------------------
# Load CSV Data
# ---------------------------------------------------------

def load_csv_data(connection):
    """Load cleaned CSV files into SQLite tables."""

    customers = pd.read_csv(
        CLEAN_DIR / "customers_clean.csv"
    )

    products = pd.read_csv(
        CLEAN_DIR / "products_clean.csv"
    )

    orders = pd.read_csv(
        CLEAN_DIR / "orders_clean.csv"
    )

    order_items = pd.read_csv(
        CLEAN_DIR / "order_items_clean.csv"
    )

    # Convert missing customer IDs to None
    orders["customer_id"] = orders[
        "customer_id"
    ].where(
        orders["customer_id"].notna(),
        None
    )

    # Load data into SQLite
    customers.to_sql(
        "customers",
        connection,
        if_exists="append",
        index=False
    )

    products.to_sql(
        "products",
        connection,
        if_exists="append",
        index=False
    )

    orders.to_sql(
        "orders",
        connection,
        if_exists="append",
        index=False
    )

    order_items.to_sql(
        "order_items",
        connection,
        if_exists="append",
        index=False
    )

    print("\nData loaded successfully.")


# ---------------------------------------------------------
# Verify Row Counts
# ---------------------------------------------------------

def verify_row_counts(connection):
    """Verify number of records in each table."""

    cursor = connection.cursor()

    tables = [
        "customers",
        "products",
        "orders",
        "order_items"
    ]

    print("\n" + "=" * 50)
    print("DATABASE ROW COUNTS")
    print("=" * 50)

    for table in tables:

        cursor.execute(
            f"SELECT COUNT(*) FROM {table}"
        )

        count = cursor.fetchone()[0]

        print(f"{table:<15} : {count}")


# ---------------------------------------------------------
# Verify Relationships
# ---------------------------------------------------------

def verify_relationships(connection):
    """Check foreign-key relationships."""

    cursor = connection.cursor()

    print("\n" + "=" * 50)
    print("RELATIONSHIP VALIDATION")
    print("=" * 50)

    # Orders with invalid customers
    cursor.execute("""
        SELECT COUNT(*)
        FROM orders o
        LEFT JOIN customers c
            ON o.customer_id = c.customer_id
        WHERE o.customer_id IS NOT NULL
          AND c.customer_id IS NULL
    """)

    invalid_customers = cursor.fetchone()[0]

    print(
        f"Orders with invalid customer_id : "
        f"{invalid_customers}"
    )

    # Order items with invalid orders
    cursor.execute("""
        SELECT COUNT(*)
        FROM order_items oi
        LEFT JOIN orders o
            ON oi.order_id = o.order_id
        WHERE o.order_id IS NULL
    """)

    invalid_orders = cursor.fetchone()[0]

    print(
        f"Items with invalid order_id      : "
        f"{invalid_orders}"
    )

    # Order items with invalid products
    cursor.execute("""
        SELECT COUNT(*)
        FROM order_items oi
        LEFT JOIN products p
            ON oi.product_id = p.product_id
        WHERE p.product_id IS NULL
    """)

    invalid_products = cursor.fetchone()[0]

    print(
        f"Items with invalid product_id    : "
        f"{invalid_products}"
    )


# ---------------------------------------------------------
# Show Table Structure
# ---------------------------------------------------------

def show_table_structure(connection):

    cursor = connection.cursor()

    print("\n" + "=" * 50)
    print("DATABASE TABLES")
    print("=" * 50)

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name
    """)

    tables = cursor.fetchall()

    for table in tables:
        print(f"- {table[0]}")


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    print("=" * 60)
    print("E-COMMERCE DATABASE LOADER")
    print("=" * 60)

    connection = create_connection()

    if connection is None:
        return

    try:

        create_tables(connection)

        load_csv_data(connection)

        verify_row_counts(connection)

        verify_relationships(connection)

        show_table_structure(connection)

        print("\n" + "=" * 60)
        print("DATABASE LOADING COMPLETED")
        print("=" * 60)

    except Exception as error:

        print(f"\nError while loading database: {error}")

    finally:

        connection.close()

        print("\nDatabase connection closed.")


if __name__ == "__main__":
    main()