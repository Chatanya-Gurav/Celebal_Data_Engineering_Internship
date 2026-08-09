# Smart Patient Readmission Risk Pipeline
# Reusable pipeline helper functions

import random
from datetime import datetime, timedelta

from pyspark.sql import DataFrame
from pyspark.sql import functions as F


# ============================================================
# SPARK CONFIGURATION
# ============================================================

def apply_spark_optimizations(spark, settings: dict) -> None:
    """Apply project Spark optimization settings."""

    print("\nApplying Spark optimizations...")

    for key, value in settings.items():
        try:
            spark.conf.set(key, value)
            print(f"  ✓ {key} = {value}")
        except Exception as exc:
            print(f"  ⚠ Could not set {key}: {exc}")

    # Delta optimized-write / auto-compaction settings.
    # Some Databricks runtimes manage these automatically,
    # so failures here should not stop the pipeline.
    optional_delta_settings = {
        "spark.databricks.delta.optimizeWrite.enabled": "true",
        "spark.databricks.delta.autoCompact.enabled": "true",
    }

    for key, value in optional_delta_settings.items():
        try:
            spark.conf.set(key, value)
        except Exception:
            pass


# ============================================================
# DATA QUALITY INJECTION
# ============================================================

def inject_nulls(
    rows: list,
    col_indices: list[int],
    rate: float,
) -> list:
    """Inject NULL values into selected columns."""

    result = [list(row) for row in rows]

    for row in result:
        for idx in col_indices:
            if random.random() < rate:
                row[idx] = None

    return result


def inject_inconsistent_categories(
    rows: list,
    col_idx: int,
    valid_values: list[str],
    noise_map: dict,
    rate: float,
) -> list:
    """Inject inconsistent categorical representations."""

    result = [list(row) for row in rows]

    for row in result:
        current_value = row[col_idx]

        if (
            current_value in valid_values
            and current_value in noise_map
            and random.random() < rate
        ):
            row[col_idx] = random.choice(noise_map[current_value])

    return result


def inject_date_noise(
    rows: list,
    col_idx: int,
    max_jitter_days: int,
    rate: float,
) -> list:
    """Add small random date noise to date strings."""

    result = [list(row) for row in rows]

    for row in result:
        if random.random() < rate and row[col_idx] is not None:

            original = datetime.strptime(
                row[col_idx],
                "%Y-%m-%d"
            ).date()

            jitter = random.randint(
                -max_jitter_days,
                max_jitter_days
            )

            row[col_idx] = (
                original + timedelta(days=jitter)
            ).isoformat()

    return result


# ============================================================
# RANDOM DATA HELPERS
# ============================================================

def weighted_choice(weighted_values):
    """
    Select from:
    [("value1", weight1), ("value2", weight2), ...]
    """

    values = [item[0] for item in weighted_values]
    weights = [item[1] for item in weighted_values]

    return random.choices(
        values,
        weights=weights,
        k=1
    )[0]


def generate_phone():
    """Generate a synthetic Indian-style phone number."""

    first_digit = random.choice(
        ["6", "7", "8", "9"]
    )

    remaining = "".join(
        random.choices(
            "0123456789",
            k=9
        )
    )

    return f"+91-{first_digit}{remaining}"


# ============================================================
# LOGGING / OBSERVABILITY
# ============================================================

def log_table_stats(spark, table_name: str) -> None:
    """Print row count and column information."""

    df = spark.table(table_name)

    print(f"\nTable: {table_name}")
    print(f"Rows: {df.count():,}")
    print(f"Columns: {len(df.columns)}")
    print(f"Column names: {df.columns}")


def log_dataframe_stats(
    df: DataFrame,
    name: str
) -> None:
    """Print DataFrame statistics."""

    print(f"\n{name}")
    print(f"Rows: {df.count():,}")
    print(f"Columns: {len(df.columns)}")
    print(f"Column names: {df.columns}")


# ============================================================
# VALIDATION
# ============================================================

def validate_no_duplicates(
    df: DataFrame,
    key_columns: list[str],
    table_name: str,
) -> None:
    """Validate that key columns contain no duplicate groups."""

    duplicate_count = (
        df.groupBy(*key_columns)
        .count()
        .filter(F.col("count") > 1)
        .count()
    )

    if duplicate_count == 0:
        print(
            f"✓ {table_name}: "
            f"No duplicate {key_columns} values."
        )
    else:
        raise ValueError(
            f"{table_name}: "
            f"Found {duplicate_count} duplicate key groups."
        )


def validate_not_empty(
    df: DataFrame,
    table_name: str,
) -> None:
    """Validate that a DataFrame contains rows."""

    count = df.count()

    if count == 0:
        raise ValueError(
            f"{table_name}: DataFrame is empty."
        )

    print(
        f"✓ {table_name}: "
        f"{count:,} rows present."
    )


# ============================================================
# DELTA WRITE
# ============================================================

def write_delta_overwrite(
    df: DataFrame,
    table_name: str,
) -> None:
    """
    Idempotent Delta write using overwrite mode
    with schema replacement.
    """

    (
        df.write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(table_name)
    )

    print(
        f"✓ Delta table written: {table_name}"
    )


# ============================================================
# DELTA OPTIMIZATION
# ============================================================

def optimize_table(
    spark,
    table_name: str,
    zorder_columns=None,
) -> None:
    """Run OPTIMIZE and optional ZORDER."""

    try:
        if zorder_columns:
            columns = ", ".join(zorder_columns)

            spark.sql(
                f"""
                OPTIMIZE {table_name}
                ZORDER BY ({columns})
                """
            )

            print(
                f"✓ OPTIMIZE + ZORDER: "
                f"{table_name}"
            )

        else:
            spark.sql(
                f"OPTIMIZE {table_name}"
            )

            print(
                f"✓ OPTIMIZE: {table_name}"
            )

    except Exception as exc:
        print(
            f"⚠ OPTIMIZE skipped for "
            f"{table_name}: {exc}"
        )


def analyze_table(
    spark,
    table_name: str,
) -> None:
    """Compute table statistics."""

    try:
        spark.sql(
            f"ANALYZE TABLE "
            f"{table_name} COMPUTE STATISTICS"
        )

        print(
            f"✓ ANALYZE TABLE: {table_name}"
        )

    except Exception as exc:
        print(
            f"⚠ ANALYZE skipped for "
            f"{table_name}: {exc}"
        )


# ============================================================
# DATA QUALITY AUDIT
# ============================================================

def null_summary(
    df: DataFrame,
    table_name: str,
) -> None:
    """Print NULL counts for every column."""

    expressions = [
        F.sum(
            F.when(
                F.col(column).isNull(),
                1
            ).otherwise(0)
        ).alias(column)
        for column in df.columns
    ]

    summary = df.select(expressions)

    print(
        f"\nNULL summary: {table_name}"
    )

    summary.show(
        truncate=False
    )