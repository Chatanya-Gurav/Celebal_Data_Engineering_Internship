# Databricks notebook source
# ============================================================
# GOLD LAYER - LOAD SILVER DATA
# ============================================================

import sys
sys.path.append("..")

import config as cfg

print("=" * 60)
print("GOLD LAYER - LOADING SILVER DATA")
print("=" * 60)

# Load Silver Delta tables
patients_silver = spark.table(
    f"{cfg.CATALOG}.{cfg.SCHEMA}.patients_silver"
)

diagnoses_silver = spark.table(
    f"{cfg.CATALOG}.{cfg.SCHEMA}.diagnoses_silver"
)

admissions_silver = spark.table(
    f"{cfg.CATALOG}.{cfg.SCHEMA}.admissions_silver"
)

print(f"Patients Silver   : {patients_silver.count()} rows")
print(f"Diagnoses Silver  : {diagnoses_silver.count()} rows")
print(f"Admissions Silver : {admissions_silver.count()} rows")

print("\nSilver tables loaded successfully.")

# COMMAND ----------

# ============================================================
# GOLD LAYER - CREATE ENRICHED ADMISSION DATASET
# ============================================================

from pyspark.sql.functions import col

print("=" * 60)
print("CREATING ENRICHED GOLD DATASET")
print("=" * 60)

# Join admissions with patient information
gold_admissions = (
    admissions_silver.alias("a")
    .join(
        patients_silver.alias("p"),
        col("a.patient_id") == col("p.patient_id"),
        "left"
    )
    .join(
        diagnoses_silver.alias("d"),
        col("a.diagnosis_id") == col("d.diagnosis_id"),
        "left"
    )
    .select(
        col("a.admission_id"),
        col("a.patient_id"),
        col("p.name"),
        col("p.age"),
        col("p.gender"),
        col("p.contact"),
        col("a.diagnosis_id"),
        col("d.icd_code"),
        col("d.category"),
        col("a.department"),
        col("a.physician"),
        col("a.admission_date"),
        col("a.discharge_date"),
        col("a.length_of_stay"),
        col("a.readmitted_within_30_days")
    )
)

print(f"Gold enriched records: {gold_admissions.count()}")
print(f"Gold columns: {len(gold_admissions.columns)}")

print("\nGold dataset schema:")
gold_admissions.printSchema()

# COMMAND ----------

# ============================================================
# GOLD LAYER - READMISSION RISK FEATURES
# ============================================================

from pyspark.sql.functions import (
    col,
    when,
    datediff,
    current_date
)

print("=" * 60)
print("CREATING READMISSION RISK FEATURES")
print("=" * 60)

gold_risk_features = (
    gold_admissions
    .withColumn(
        "age_group",
        when(col("age") < 18, "Pediatric")
        .when(col("age") < 40, "Young Adult")
        .when(col("age") < 60, "Middle Age")
        .otherwise("Senior")
    )
    .withColumn(
        "stay_category",
        when(col("length_of_stay") <= 2, "Short Stay")
        .when(col("length_of_stay") <= 7, "Medium Stay")
        .otherwise("Long Stay")
    )
    .withColumn(
        "readmission_risk",
        when(col("readmitted_within_30_days") == 1, "High")
        .otherwise("Low")
    )
)

print(f"Risk feature records: {gold_risk_features.count()}")
print(f"Risk feature columns: {len(gold_risk_features.columns)}")

print("\nReadmission risk distribution:")
gold_risk_features.groupBy("readmission_risk").count().show()

print("\nAge group distribution:")
gold_risk_features.groupBy("age_group").count().show()

print("\nStay category distribution:")
gold_risk_features.groupBy("stay_category").count().show()

print("\nReadmission risk features created successfully.")

# COMMAND ----------

# ============================================================
# GOLD LAYER - WRITE GOLD DELTA TABLE
# ============================================================

print("=" * 60)
print("WRITING GOLD DELTA TABLE")
print("=" * 60)

gold_table = "workspace.smart_patient_readmission.readmission_risk_gold"

gold_risk_features.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable(gold_table)

print(f"Created: {gold_table}")
print("\nGOLD DELTA TABLE CREATED SUCCESSFULLY.")

# COMMAND ----------

# ============================================================
# VERIFY GOLD DELTA TABLE
# ============================================================

print("=" * 60)
print("VERIFYING GOLD DELTA TABLE")
print("=" * 60)

gold_table_df = spark.table(
    "workspace.smart_patient_readmission.readmission_risk_gold"
)

print(f"Gold records : {gold_table_df.count()}")
print(f"Gold columns : {len(gold_table_df.columns)}")

print("\nGold table columns:")
print(gold_table_df.columns)

print("\nSample Gold records:")
gold_table_df.show(5, truncate=False)

print("\nGold table verified successfully.")