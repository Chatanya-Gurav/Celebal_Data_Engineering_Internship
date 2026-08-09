# Databricks notebook source
# ============================================================
# SILVER LAYER - LOAD BRONZE TABLES
# ============================================================

from pyspark.sql import functions as F

CATALOG = "workspace"
SCHEMA = "smart_patient_readmission"

print("=" * 60)
print("LOADING BRONZE TABLES")
print("=" * 60)

patients_bronze = spark.table(
    f"{CATALOG}.{SCHEMA}.patients_bronze"
)

diagnoses_bronze = spark.table(
    f"{CATALOG}.{SCHEMA}.diagnoses_bronze"
)

admissions_bronze = spark.table(
    f"{CATALOG}.{SCHEMA}.admissions_bronze"
)

print(f"Patients Bronze    : {patients_bronze.count()} rows")
print(f"Diagnoses Bronze   : {diagnoses_bronze.count()} rows")
print(f"Admissions Bronze  : {admissions_bronze.count()} rows")

print("\nBronze tables loaded successfully.")

# COMMAND ----------

# ============================================================
# SILVER LAYER - CLEAN AND STANDARDIZE DATA
# ============================================================

print("=" * 60)
print("CLEANING AND STANDARDIZING SILVER DATA")
print("=" * 60)

# -----------------------------
# Patients
# -----------------------------
patients_silver = (
    patients_bronze
    .select(
        F.col("patient_id").cast("string"),
        F.trim(F.col("name")).alias("name"),
        F.col("age").cast("int"),
        F.initcap(F.trim(F.col("gender"))).alias("gender"),
        F.trim(F.col("contact")).alias("contact")
    )
    .dropDuplicates(["patient_id"])
)

# -----------------------------
# Diagnoses
# -----------------------------
diagnoses_silver = (
    diagnoses_bronze
    .select(
        F.col("diagnosis_id").cast("string"),
        F.upper(F.trim(F.col("icd_code"))).alias("icd_code"),
        F.initcap(F.trim(F.col("category"))).alias("category")
    )
    .dropDuplicates(["diagnosis_id"])
)

# -----------------------------
# Admissions
# -----------------------------
admissions_silver = (
    admissions_bronze
    .select(
        F.col("admission_id").cast("string"),
        F.col("patient_id").cast("string"),
        F.col("diagnosis_id").cast("string"),
        F.initcap(F.trim(F.col("department"))).alias("department"),
        F.initcap(F.trim(F.col("physician"))).alias("physician"),
        F.to_date("admission_date").alias("admission_date"),
        F.to_date("discharge_date").alias("discharge_date"),
        F.col("length_of_stay").cast("int").alias("length_of_stay"),
        F.col("readmitted_within_30_days").cast("int").alias(
            "readmitted_within_30_days"
        )
    )
    .dropDuplicates(["admission_id"])
)

print(f"Patients Silver   : {patients_silver.count()} rows")
print(f"Diagnoses Silver  : {diagnoses_silver.count()} rows")
print(f"Admissions Silver : {admissions_silver.count()} rows")

print("\nSilver cleaning completed successfully.")

# COMMAND ----------

# ============================================================
# WRITE SILVER DELTA TABLES
# ============================================================

print("=" * 60)
print("WRITING SILVER DELTA TABLES")
print("=" * 60)

patients_silver.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable(f"{CATALOG}.{SCHEMA}.patients_silver")

diagnoses_silver.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable(f"{CATALOG}.{SCHEMA}.diagnoses_silver")

admissions_silver.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable(f"{CATALOG}.{SCHEMA}.admissions_silver")

print("Created:", f"{CATALOG}.{SCHEMA}.patients_silver")
print("Created:", f"{CATALOG}.{SCHEMA}.diagnoses_silver")
print("Created:", f"{CATALOG}.{SCHEMA}.admissions_silver")

print("\nSILVER DELTA TABLES CREATED SUCCESSFULLY.")

# COMMAND ----------

# ============================================================
# VERIFY SILVER DELTA TABLES
# ============================================================

print("=" * 60)
print("VERIFYING SILVER DELTA TABLES")
print("=" * 60)

print("Patients Silver   :", spark.table(f"{CATALOG}.{SCHEMA}.patients_silver").count())
print("Diagnoses Silver  :", spark.table(f"{CATALOG}.{SCHEMA}.diagnoses_silver").count())
print("Admissions Silver :", spark.table(f"{CATALOG}.{SCHEMA}.admissions_silver").count())

print("\nSilver tables verified successfully.")

# COMMAND ----------

# ============================================================
# LOAD SILVER TABLES FOR GOLD TRANSFORMATION
# ============================================================

print("=" * 60)
print("LOADING SILVER TABLES FOR GOLD LAYER")
print("=" * 60)

patients_silver = spark.table(
    f"{CATALOG}.{SCHEMA}.patients_silver"
)

diagnoses_silver = spark.table(
    f"{CATALOG}.{SCHEMA}.diagnoses_silver"
)

admissions_silver = spark.table(
    f"{CATALOG}.{SCHEMA}.admissions_silver"
)

print(f"Patients Silver   : {patients_silver.count()} rows")
print(f"Diagnoses Silver  : {diagnoses_silver.count()} rows")
print(f"Admissions Silver : {admissions_silver.count()} rows")

print("\nSilver data loaded successfully for Gold transformation.")