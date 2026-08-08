import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
CLEAN_DIR = BASE_DIR / "data" / "cleaned"
OUTPUT_DIR = BASE_DIR / "output"

CLEAN_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CUSTOMERS_RAW = RAW_DIR / "customers.csv"
PRODUCTS_RAW = RAW_DIR / "products.csv"
ORDERS_RAW = RAW_DIR / "orders.csv"
ORDER_ITEMS_RAW = RAW_DIR / "order_items.csv"

CUSTOMERS_CLEAN = CLEAN_DIR / "customers_clean.csv"
PRODUCTS_CLEAN = CLEAN_DIR / "products_clean.csv"
ORDERS_CLEAN = CLEAN_DIR / "orders_clean.csv"
ORDER_ITEMS_CLEAN = CLEAN_DIR / "order_items_clean.csv"

ISSUES_REPORT = OUTPUT_DIR / "issues_report.txt"


# Store all data-quality issues found during cleaning
issues = []


# ---------------------------------------------------------
# 1. Clean Orders
# ---------------------------------------------------------

def clean_orders():
    print("\nCleaning orders...")

    df = pd.read_csv(ORDERS_RAW)

    original_count = len(df)

    # Check duplicate orders
    duplicate_count = df.duplicated(subset=["order_id"]).sum()

    if duplicate_count > 0:
        issues.append(
            f"Orders: {duplicate_count} duplicate order_id records found."
        )

        df = df.drop_duplicates(
            subset=["order_id"],
            keep="first"
        )

    # Count missing customer IDs
    missing_customer_ids = df["customer_id"].isna().sum()

    if missing_customer_ids > 0:
        issues.append(
            f"Orders: {missing_customer_ids} missing customer_id values found."
        )

    # Convert blank strings to NULL/NaN
    df["customer_id"] = df["customer_id"].replace(
        r"^\s*$",
        pd.NA,
        regex=True
    )

    # Convert dates.
    # The generated dataset contains both:
    # YYYY-MM-DD HH:MM:SS
    # DD-MM-YYYY HH:MM:SS

    df["order_date"] = pd.to_datetime(
        df["order_date"],
        format="mixed",
        dayfirst=True,
        errors="coerce"
    )

    invalid_dates = df["order_date"].isna().sum()

    if invalid_dates > 0:
        issues.append(
            f"Orders: {invalid_dates} invalid order_date values found."
        )

    # Standardize date format
    df["order_date"] = df["order_date"].dt.strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # Remove rows with invalid order IDs
    missing_order_ids = df["order_id"].isna().sum()

    if missing_order_ids > 0:
        issues.append(
            f"Orders: {missing_order_ids} rows with missing order_id removed."
        )

        df = df.dropna(subset=["order_id"])

    df.to_csv(
        ORDERS_CLEAN,
        index=False
    )

    print(f"Original rows: {original_count}")
    print(f"Cleaned rows:  {len(df)}")
    print(f"Saved: {ORDERS_CLEAN}")

    return df


# ---------------------------------------------------------
# 2. Clean Products
# ---------------------------------------------------------

def clean_products():
    print("\nCleaning products...")

    df = pd.read_csv(PRODUCTS_RAW)

    original_count = len(df)

    # Check duplicate product IDs
    duplicate_count = df.duplicated(
        subset=["product_id"]
    ).sum()

    if duplicate_count > 0:
        issues.append(
            f"Products: {duplicate_count} duplicate product_id records found."
        )

        df = df.drop_duplicates(
            subset=["product_id"],
            keep="first"
        )

    # Count product names requiring normalization
    original_names = df["product_name"].copy()

    # Remove extra spaces
    df["product_name"] = (
        df["product_name"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    changed_names = (
        original_names.astype(str) != df["product_name"]
    ).sum()

    if changed_names > 0:
        issues.append(
            f"Products: {changed_names} product names normalized "
            f"(spaces/capitalization)."
        )

    # Convert cost price to numeric
    df["cost_price"] = pd.to_numeric(
        df["cost_price"],
        errors="coerce"
    )

    invalid_prices = df["cost_price"].isna().sum()

    if invalid_prices > 0:
        issues.append(
            f"Products: {invalid_prices} invalid cost_price values found."
        )

    df.to_csv(
        PRODUCTS_CLEAN,
        index=False
    )

    print(f"Original rows: {original_count}")
    print(f"Cleaned rows:  {len(df)}")
    print(f"Saved: {PRODUCTS_CLEAN}")

    return df


# ---------------------------------------------------------
# 3. Validate Emails
# ---------------------------------------------------------

def validate_emails():
    print("\nValidating customer emails...")

    df = pd.read_csv(CUSTOMERS_RAW)

    # Basic email validation:
    # something@something.domain

    email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    valid_emails = df["email"].astype(str).str.match(
        email_pattern,
        na=False
    )

    invalid_df = df[~valid_emails]

    invalid_customer_ids = invalid_df[
        "customer_id"
    ].tolist()

    if len(invalid_customer_ids) > 0:
        issues.append(
            f"Customers: {len(invalid_customer_ids)} invalid emails found."
        )

        issues.append(
            "Invalid customer IDs: "
            + ", ".join(map(str, invalid_customer_ids))
        )

    print(f"Invalid emails found: {len(invalid_customer_ids)}")

    return invalid_customer_ids


# ---------------------------------------------------------
# 4. Check Referential Integrity
# ---------------------------------------------------------

def check_referential_integrity():
    print("\nChecking referential integrity...")

    orders = pd.read_csv(ORDERS_RAW)
    order_items = pd.read_csv(ORDER_ITEMS_RAW)

    valid_order_ids = set(
        orders["order_id"].dropna()
    )

    invalid_items = order_items[
        ~order_items["order_id"].isin(valid_order_ids)
    ]

    invalid_count = len(invalid_items)

    if invalid_count > 0:
        issues.append(
            f"Order Items: {invalid_count} records reference "
            f"non-existent order IDs."
        )

        invalid_order_ids = (
            invalid_items["order_id"]
            .drop_duplicates()
            .tolist()
        )

        issues.append(
            "Invalid order IDs: "
            + ", ".join(map(str, invalid_order_ids))
        )

    print(
        f"Invalid order references found: {invalid_count}"
    )

    return invalid_items


# ---------------------------------------------------------
# 5. Clean Customers
# ---------------------------------------------------------

def clean_customers():
    print("\nCleaning customers...")

    df = pd.read_csv(CUSTOMERS_RAW)

    original_count = len(df)

    # Remove duplicate customer IDs
    duplicate_count = df.duplicated(
        subset=["customer_id"]
    ).sum()

    if duplicate_count > 0:
        issues.append(
            f"Customers: {duplicate_count} duplicate customer_id records found."
        )

        df = df.drop_duplicates(
            subset=["customer_id"],
            keep="first"
        )

    # Clean names
    df["customer_name"] = (
        df["customer_name"]
        .astype(str)
        .str.strip()
    )

    # Standardize registration date
    df["registration_date"] = pd.to_datetime(
        df["registration_date"],
        errors="coerce"
    ).dt.strftime("%Y-%m-%d")

    # Save cleaned customers
    df.to_csv(
        CUSTOMERS_CLEAN,
        index=False
    )

    print(f"Original rows: {original_count}")
    print(f"Cleaned rows:  {len(df)}")
    print(f"Saved: {CUSTOMERS_CLEAN}")

    return df


# ---------------------------------------------------------
# 6. Clean Order Items
# ---------------------------------------------------------

def clean_order_items():
    print("\nCleaning order items...")

    df = pd.read_csv(ORDER_ITEMS_RAW)

    original_count = len(df)

    # Convert numeric columns
    df["quantity"] = pd.to_numeric(
        df["quantity"],
        errors="coerce"
    )

    df["unit_price"] = pd.to_numeric(
        df["unit_price"],
        errors="coerce"
    )

    df["discount_percent"] = pd.to_numeric(
        df["discount_percent"],
        errors="coerce"
    )

    # Negative quantities represent returns according
    # to the project specification.
    negative_quantity_count = (
        df["quantity"] < 0
    ).sum()

    if negative_quantity_count > 0:
        issues.append(
            f"Order Items: {negative_quantity_count} negative "
            f"quantity values found (returns)."
        )

    # Check invalid discount percentages
    invalid_discount_count = (
        (df["discount_percent"] < 0)
        | (df["discount_percent"] > 100)
    ).sum()

    if invalid_discount_count > 0:
        issues.append(
            f"Order Items: {invalid_discount_count} invalid "
            f"discount_percent values found."
        )

        # Keep discount inside valid range
        df["discount_percent"] = df[
            "discount_percent"
        ].clip(0, 100)

    # Check zero quantities
    zero_quantity_count = (
        df["quantity"] == 0
    ).sum()

    if zero_quantity_count > 0:
        issues.append(
            f"Order Items: {zero_quantity_count} zero quantity "
            f"values found."
        )

    # Remove rows with missing essential fields
    missing_item_fields = df[
        df["item_id"].isna()
        | df["order_id"].isna()
        | df["product_id"].isna()
    ]

    if len(missing_item_fields) > 0:
        issues.append(
            f"Order Items: {len(missing_item_fields)} rows with "
            f"missing required IDs removed."
        )

        df = df.dropna(
            subset=[
                "item_id",
                "order_id",
                "product_id"
            ]
        )

    # Remove order items that reference non-existent orders
    orders = pd.read_csv(ORDERS_RAW)

    valid_order_ids = set(
        orders["order_id"].dropna()
    )

    invalid_reference_rows = ~df["order_id"].isin(
        valid_order_ids
    )

    invalid_reference_count = invalid_reference_rows.sum()

    if invalid_reference_count > 0:
        issues.append(
            f"Order Items: {invalid_reference_count} invalid "
            f"order references removed from cleaned data."
        )

        df = df[~invalid_reference_rows]

    # Save cleaned order items
    df.to_csv(
        ORDER_ITEMS_CLEAN,
        index=False
    )

    print(f"Original rows: {original_count}")
    print(f"Cleaned rows:  {len(df)}")
    print(f"Saved: {ORDER_ITEMS_CLEAN}")

    return df


# ---------------------------------------------------------
# 7. Write Issues Report
# ---------------------------------------------------------

def write_issues_report():
    print("\nWriting issues report...")

    with open(
        ISSUES_REPORT,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "E-COMMERCE DATA QUALITY ISSUES REPORT\n"
        )

        file.write(
            "=" * 50 + "\n\n"
        )

        if not issues:
            file.write(
                "No data quality issues were found.\n"
            )
        else:
            for number, issue in enumerate(
                issues,
                start=1
            ):
                file.write(
                    f"{number}. {issue}\n"
                )

    print(f"Saved: {ISSUES_REPORT}")


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    print("=" * 60)
    print("E-COMMERCE DATA CLEANING")
    print("=" * 60)

    # Run validation functions
    validate_emails()
    check_referential_integrity()

    # Clean datasets
    clean_customers()
    clean_products()
    clean_orders()
    clean_order_items()

    # Generate issue report
    write_issues_report()

    print("\n" + "=" * 60)
    print("DATA CLEANING COMPLETED")
    print("=" * 60)

    print("\nCleaned files:")
    print(f"1. {CUSTOMERS_CLEAN}")
    print(f"2. {PRODUCTS_CLEAN}")
    print(f"3. {ORDERS_CLEAN}")
    print(f"4. {ORDER_ITEMS_CLEAN}")
    print(f"5. {ISSUES_REPORT}")


if __name__ == "__main__":
    main()