import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

from faker import Faker


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

fake = Faker()
random.seed(42)
Faker.seed(42)

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

CUSTOMERS_FILE = RAW_DIR / "customers.csv"
PRODUCTS_FILE = RAW_DIR / "products.csv"
ORDERS_FILE = RAW_DIR / "orders.csv"
ORDER_ITEMS_FILE = RAW_DIR / "order_items.csv"


# At least 500 rows are required for every dataset
NUM_CUSTOMERS = 600
NUM_PRODUCTS = 600
NUM_ORDERS = 1200
NUM_ORDER_ITEMS = 2500


# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------

def random_date(start_date, end_date):
    """Generate a random datetime between two dates."""
    delta = end_date - start_date
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start_date + timedelta(seconds=random_seconds)


def write_csv(file_path, fieldnames, rows):
    """Write a list of dictionaries to CSV."""
    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


# ---------------------------------------------------------
# 1. Generate Customers
# ---------------------------------------------------------

def generate_customers():
    customers = []

    customer_types = ["REGULAR", "PREMIUM", "VIP"]

    start_date = datetime(2023, 1, 1)
    end_date = datetime(2026, 7, 31)

    for i in range(1, NUM_CUSTOMERS + 1):

        customer_id = f"CUST{i:04d}"

        name = fake.name()

        # 2% invalid emails
        if random.random() < 0.02:
            invalid_email_type = random.choice([
                "missing_at",
                "missing_domain"
            ])

            if invalid_email_type == "missing_at":
                email = fake.user_name() + ".com"
            else:
                email = fake.user_name() + "@"
        else:
            email = fake.email()

        registration_date = random_date(start_date, end_date)

        customer_type = random.choices(
            customer_types,
            weights=[70, 25, 5],
            k=1
        )[0]

        customers.append({
            "customer_id": customer_id,
            "customer_name": name,
            "email": email,
            "registration_date": registration_date.strftime("%Y-%m-%d"),
            "customer_type": customer_type
        })

    write_csv(
        CUSTOMERS_FILE,
        [
            "customer_id",
            "customer_name",
            "email",
            "registration_date",
            "customer_type"
        ],
        customers
    )

    print(f"Created {CUSTOMERS_FILE}")
    print(f"Customers: {len(customers)}")

    return customers


# ---------------------------------------------------------
# 2. Generate Products
# ---------------------------------------------------------

def generate_products():
    products = []

    categories = {
        "Electronics": [
            "Laptop",
            "Smartphone",
            "Headphones",
            "Keyboard",
            "Mouse",
            "Monitor",
            "Smart Watch"
        ],
        "Clothing": [
            "T-Shirt",
            "Jeans",
            "Jacket",
            "Sneakers",
            "Hoodie",
            "Dress",
            "Shirt"
        ],
        "Home": [
            "Chair",
            "Table",
            "Lamp",
            "Bedsheet",
            "Pillow",
            "Cookware",
            "Storage Box"
        ],
        "Books": [
            "Python Programming",
            "Data Engineering",
            "Machine Learning",
            "Database Systems",
            "Cloud Computing",
            "Web Development",
            "Cyber Security"
        ]
    }

    subcategories = {
        "Electronics": [
            "Computers",
            "Mobile",
            "Accessories"
        ],
        "Clothing": [
            "Men",
            "Women",
            "Footwear"
        ],
        "Home": [
            "Furniture",
            "Kitchen",
            "Decor"
        ],
        "Books": [
            "Technology",
            "Programming",
            "Education"
        ]
    }

    for i in range(1, NUM_PRODUCTS + 1):

        product_id = f"PROD{i:04d}"

        category = random.choice(list(categories.keys()))

        base_name = random.choice(categories[category])

        # Generate a realistic product name
        product_name = f"{base_name} {random.randint(1, 100)}"

        # Intentionally introduce spaces / mixed case
        issue_probability = random.random()

        if issue_probability < 0.04:
            product_name = "  " + product_name + "  "

        elif issue_probability < 0.08:
            product_name = product_name.upper()

        elif issue_probability < 0.12:
            product_name = product_name.lower()

        subcategory = random.choice(subcategories[category])

        cost_price = round(random.uniform(100, 50000), 2)

        products.append({
            "product_id": product_id,
            "product_name": product_name,
            "category": category,
            "subcategory": subcategory,
            "cost_price": cost_price
        })

    write_csv(
        PRODUCTS_FILE,
        [
            "product_id",
            "product_name",
            "category",
            "subcategory",
            "cost_price"
        ],
        products
    )

    print(f"Created {PRODUCTS_FILE}")
    print(f"Products: {len(products)}")

    return products


# ---------------------------------------------------------
# 3. Generate Orders
# ---------------------------------------------------------

def generate_orders(customers):
    orders = []

    customer_ids = [customer["customer_id"] for customer in customers]

    statuses = [
        "PLACED",
        "SHIPPED",
        "DELIVERED",
        "CANCELLED",
        "RETURNED"
    ]

    regions = [
        "NORTH",
        "SOUTH",
        "EAST",
        "WEST",
        "CENTRAL"
    ]

    start_date = datetime(2024, 1, 1)
    end_date = datetime(2026, 7, 31)

    for i in range(1, NUM_ORDERS + 1):

        order_id = f"ORD{i:05d}"

        # 5% NULL customer_id
        if random.random() < 0.05:
            customer_id = ""
        else:
            customer_id = random.choice(customer_ids)

        order_date = random_date(start_date, end_date)

        # Intentionally introduce wrong date format
        if random.random() < 0.05:
            formatted_date = order_date.strftime("%d-%m-%Y %H:%M:%S")
        else:
            formatted_date = order_date.strftime("%Y-%m-%d %H:%M:%S")

        status = random.choices(
            statuses,
            weights=[15, 15, 50, 10, 10],
            k=1
        )[0]

        region_code = random.choice(regions)

        orders.append({
            "order_id": order_id,
            "customer_id": customer_id,
            "order_date": formatted_date,
            "status": status,
            "region_code": region_code
        })

    write_csv(
        ORDERS_FILE,
        [
            "order_id",
            "customer_id",
            "order_date",
            "status",
            "region_code"
        ],
        orders
    )

    print(f"Created {ORDERS_FILE}")
    print(f"Orders: {len(orders)}")

    return orders


# ---------------------------------------------------------
# 4. Generate Order Items
# ---------------------------------------------------------

def generate_order_items(orders, products):
    order_items = []

    order_ids = [order["order_id"] for order in orders]
    product_ids = [product["product_id"] for product in products]

    for i in range(1, NUM_ORDER_ITEMS + 1):

        item_id = f"ITEM{i:06d}"

        # Normally use a valid order ID
        order_id = random.choice(order_ids)

        # Introduce a small number of invalid order IDs
        # so referential integrity checking can be demonstrated.
        if i % 250 == 0:
            order_id = f"INVALID_ORDER_{i}"

        product_id = random.choice(product_ids)

        # 3% negative quantities = returns
        if random.random() < 0.03:
            quantity = -random.randint(1, 5)
        else:
            quantity = random.randint(1, 8)

        unit_price = round(random.uniform(100, 50000), 2)

        discount_percent = round(
            random.uniform(0, 50),
            2
        )

        order_items.append({
            "item_id": item_id,
            "order_id": order_id,
            "product_id": product_id,
            "quantity": quantity,
            "unit_price": unit_price,
            "discount_percent": discount_percent
        })

    write_csv(
        ORDER_ITEMS_FILE,
        [
            "item_id",
            "order_id",
            "product_id",
            "quantity",
            "unit_price",
            "discount_percent"
        ],
        order_items
    )

    print(f"Created {ORDER_ITEMS_FILE}")
    print(f"Order items: {len(order_items)}")

    return order_items


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    print("=" * 60)
    print("E-COMMERCE DATA GENERATION")
    print("=" * 60)

    print("\nGenerating customers...")
    customers = generate_customers()

    print("\nGenerating products...")
    products = generate_products()

    print("\nGenerating orders...")
    orders = generate_orders(customers)

    print("\nGenerating order items...")
    generate_order_items(orders, products)

    print("\n" + "=" * 60)
    print("DATA GENERATION COMPLETED")
    print("=" * 60)

    print("\nGenerated files:")
    print(f"1. {CUSTOMERS_FILE}")
    print(f"2. {PRODUCTS_FILE}")
    print(f"3. {ORDERS_FILE}")
    print(f"4. {ORDER_ITEMS_FILE}")


if __name__ == "__main__":
    main()