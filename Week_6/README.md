# Week 6 - Spark Introduction


---

## Overview

This assignment covers the basics of Apache Spark and its use in data processing. It includes Spark architecture, Lazy Evaluation, DataFrame operations, CSV and Parquet file handling, filtering, transformations, actions, and Spark optimization concepts.

The practical tasks were performed using PySpark in Databricks.

---

## Topics Covered

- Spark Architecture - Driver, Cluster Manager and Executor
- Lazy Evaluation
- CSV File Reading with Schema Inference
- CSV vs Parquet
- DataFrame Filtering and Selection
- Renaming Columns
- Type Casting
- Lineage Graph (DAG)
- Predicate Pushdown
- Adding New Columns
- Transformations and Actions
- Reading and Writing Parquet Files
- Client Mode vs Cluster Mode
- Conditional Filtering
- `show()` vs `collect()`

---

## Practical Tasks

### 1. CSV File Reading

Read a CSV file using Spark with header and schema inference enabled.

```python
df = spark.read.csv(
    "/Volumes/workspace/default/week6/source_csv",
    header=True,
    inferSchema=True
)

df.show()
```

### 2. Filtering and Selecting Columns

Filtered products belonging to the Electronics category and selected `product_id` and `price`.

```python
df.filter(df.category == "Electronics") \
  .select("product_id", "price") \
  .show()
```

### 3. Rename Column and Type Casting

Renamed `old_name` to `new_name` and converted the `price` column to Double.

```python
df_q6 = df_q6.withColumnRenamed("old_name", "new_name") \
             .withColumn("price", df_q6["price"].cast("double"))
```

### 4. Filtering Orders

Filtered completed orders having an amount greater than 1000.

```python
df_orders.filter(
    (df_orders.status == "Completed") & (df_orders.amount > 1000)
).show()
```

### 5. Adding Final Price

Added a new `final_price` column by applying 18% tax to the base price.

```python
df_price = df_price.withColumn(
    "final_price", df_price["base_price"] * 1.18
)
```

### 6. Parquet to CSV Processing

Read data from a Parquet file, removed records where `user_id` was null, and saved the processed data in CSV format.

```python
df = spark.read.parquet(
    "/Volumes/workspace/default/week6/input_parquet"
)

df = df.filter(df.user_id.isNotNull())

df.write.mode("overwrite").option("header", True).csv(
    "/Volumes/workspace/default/week6/output_csv"
)
```

### 7. OR Condition Filtering

Filtered records where the region is `North` or the priority is `High`.

```python
df_region.filter(
    (df_region.region == "North") | (df_region.priority == "High")
).show()
```

---

## Key Learnings

- Understood the basic architecture of Apache Spark.
- Learned how Lazy Evaluation helps optimize Spark jobs.
- Worked with Spark DataFrames using PySpark.
- Performed filtering, selection, column renaming and type casting.
- Learned the difference between CSV and Parquet formats.
- Understood DAG, Predicate Pushdown and Spark fault tolerance.
- Practiced reading, transforming and writing datasets using Spark.
- Learned why `show()` is safer than `collect()` for large datasets.

---

## Tools Used

- Apache Spark
- PySpark
- Databricks
- Python

---

## Databricks Notebook

The practical implementation and execution of the Spark tasks were performed using Databricks.

**Notebook Link:**  
https://dbc-c2470b3e-08ac.cloud.databricks.com/editor/notebooks/1204010025288104?o=7474647916943129

---

## Assignment Files

- `Week6_Chaitanya_Gurav.docx` - Contains answers to all 15 questions along with execution results and screenshots.
- `README.md` - Contains the summary and practical implementation details of the Week 6 assignment.

---

## Conclusion

This assignment helped me understand the fundamentals of Apache Spark and how Spark processes large datasets efficiently. I also got practical experience with PySpark DataFrames, filtering, transformations, CSV and Parquet file handling, and basic Spark optimization concepts.