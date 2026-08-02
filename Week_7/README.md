# Week 7 - Delta Lake Operations using Databricks

## Celebal Technologies - Data Engineering Internship

**Name:** Chaitanya Gurav

---

# Objective

The objective of this assignment is to perform incremental data processing using Delta Lake in Databricks. The assignment demonstrates loading data into a Delta table, performing data cleaning, applying Update, Insert, Delete and MERGE operations, validating the results, and displaying the final dataset.

---

# Tools & Technologies

- Databricks Community Edition
- Apache Spark (PySpark)
- Delta Lake
- Python
- CSV Dataset

---

# Databricks Notebook

**Notebook Link:**

https://dbc-c2470b3e-08ac.cloud.databricks.com/editor/notebooks/3187271907670708?o=7474647916943129

---

# Dataset

- Sample - Superstore.csv
- customer_incremental.csv (Generated during the assignment)

---

# Assignment Workflow

## Step 1 - Load Dataset into Delta Lake

- Loaded the Superstore dataset into Spark DataFrame.
- Stored the dataset as a Delta Table.
- Verified schema and data.

---

## Step 2 - Data Cleaning

- Checked for NULL values.
- Removed duplicate records.
- Verified cleaned dataset.

---

## Step 3 - Update Operation

- Updated an existing record in the Delta Table.
- Verified updated values.

---

## Step 4 - Insert Operation

- Inserted a new record into the Delta Table.
- Verified inserted record.

---

## Step 5 - Delete Operation

- Deleted the inserted record.
- Verified successful deletion.

---

## Step 6 - Incremental Dataset

- Created an incremental customer dataset.
- Saved the dataset as a Delta Table.
- Exported the dataset as **customer_incremental.csv**.

---

## Step 7 - MERGE Operation

Performed MERGE operation using Delta Lake.

- Updated existing customer records.
- Inserted new customer records.

---

## Step 8 - Validation

Performed validation after MERGE.

- Verified merged records.
- Checked total row count.
- Verified duplicate Customer_ID values.

---

## Step 9 - Final Output

- Displayed the final Delta Table.
- Generated assignment summary.

---

# Project Structure

```text
Week_7/
│
├── data/
│   ├── Sample - Superstore.csv
│   └── customer_incremental.csv
│
├── Week7_Chaitanya_Gurav.ipynb
│
├── screenshots/
│   ├── data_loading/
│   │   ├── data_loaded.png
│   │   └── schema.png
│   │
│   ├── data_cleaning/
│   │   ├── null_values.png
│   │   └── remove_duplicates.png
│   │
│   ├── merge_operation/
│   │   ├── delta_table.png
│   │   ├── delta_table_created.png
│   │   ├── update_operation.png
│   │   ├── verify_insert_record.png
│   │   ├── delete_operation.png
│   │   ├── verify_delete_record.png
│   │   ├── create_incremental_dataset.png
│   │   ├── incremental_saved.png
│   │   └── merge_operation.png
│   │
│   ├── validation/
│   │   ├── merge_validation.png
│   │   ├── row_count_validation.png
│   │   └── duplicate_check.png
│   │
│   └── final_output/
│       ├── final_delta_table.png
│       └── assignment_summary.png
│
│
├── README.md
│
```

---

# Screenshots Included

## Data Loading

- Dataset Loaded
- Schema Verification

## Data Cleaning

- NULL Value Check
- Duplicate Removal

## Delta Lake Operations

- Delta Table Creation
- Update Operation
- Insert Operation
- Delete Operation
- Incremental Dataset Creation
- MERGE Operation

## Validation

- MERGE Validation
- Row Count Validation
- Duplicate Check

## Final Output

- Final Delta Table
- Assignment Summary

---

# Results

- Successfully loaded the dataset into Delta Lake.
- Cleaned the dataset.
- Performed Update, Insert and Delete operations.
- Created incremental dataset.
- Successfully applied MERGE operation.
- Validated the final dataset.
- Displayed final output.

---

# Conclusion

This assignment demonstrates how Delta Lake supports incremental data processing using Apache Spark. Delta Lake provides ACID transactions, efficient MERGE operations, and reliable data management for modern data engineering workflows. The assignment successfully completed all required operations and validated the final dataset.

