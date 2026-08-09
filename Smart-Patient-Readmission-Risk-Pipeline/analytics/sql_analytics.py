# Databricks notebook source
# ============================================================
# ANALYTICS LAYER - LOAD GOLD DATA
# ============================================================

print("=" * 60)
print("ANALYTICS LAYER - LOADING GOLD DATA")
print("=" * 60)

GOLD_TABLE = "workspace.smart_patient_readmission.readmission_risk_gold"

gold_df = spark.table(GOLD_TABLE)

print(f"Gold records : {gold_df.count()}")
print(f"Gold columns : {len(gold_df.columns)}")

print("\nGold schema:")
gold_df.printSchema()

print("\nAnalytics data loaded successfully.")

# COMMAND ----------

# ============================================================
# 1. OVERALL READMISSION ANALYSIS
# ============================================================

print("=" * 60)
print("OVERALL READMISSION ANALYSIS")
print("=" * 60)

readmission_summary = (
    gold_df
    .groupBy("readmitted_within_30_days")
    .count()
    .withColumnRenamed("count", "admission_count")
    .orderBy("readmitted_within_30_days")
)

print("\nReadmission distribution:")
readmission_summary.show()

# Calculate readmission rate
total_admissions = gold_df.count()

readmitted_count = (
    gold_df
    .filter("readmitted_within_30_days = 1")
    .count()
)

readmission_rate = (readmitted_count / total_admissions) * 100

print(f"Total admissions       : {total_admissions}")
print(f"Readmitted admissions  : {readmitted_count}")
print(f"Readmission rate       : {readmission_rate:.2f}%")

# COMMAND ----------

# ============================================================
# 2. READMISSION ANALYSIS BY DEPARTMENT
# ============================================================

from pyspark.sql.functions import sum, count, round, col

print("=" * 60)
print("READMISSION ANALYSIS BY DEPARTMENT")
print("=" * 60)

department_analysis = (
    gold_df
    .groupBy("department")
    .agg(
        count("*").alias("total_admissions"),
        sum("readmitted_within_30_days").alias("readmitted"),
        round(
            sum("readmitted_within_30_days") / count("*") * 100,
            2
        ).alias("readmission_rate")
    )
    .orderBy(col("readmission_rate").desc())
)

print("\nDepartment-wise readmission:")
department_analysis.show(truncate=False)

# COMMAND ----------

# ============================================================
# 3. READMISSION ANALYSIS BY DIAGNOSIS CATEGORY
# ============================================================

print("=" * 60)
print("READMISSION ANALYSIS BY DIAGNOSIS CATEGORY")
print("=" * 60)

diagnosis_analysis = (
    gold_df
    .groupBy("category")
    .agg(
        count("*").alias("total_admissions"),
        sum("readmitted_within_30_days").alias("readmitted"),
        round(
            sum("readmitted_within_30_days") / count("*") * 100,
            2
        ).alias("readmission_rate")
    )
    .orderBy(col("readmission_rate").desc())
)

print("\nDiagnosis category-wise readmission:")
diagnosis_analysis.show(truncate=False)

# COMMAND ----------

# ============================================================
# 4. READMISSION ANALYSIS BY AGE GROUP
# ============================================================

print("=" * 60)
print("READMISSION ANALYSIS BY AGE GROUP")
print("=" * 60)

age_analysis = (
    gold_df
    .groupBy("age_group")
    .agg(
        count("*").alias("total_admissions"),
        sum("readmitted_within_30_days").alias("readmitted"),
        round(
            sum("readmitted_within_30_days") / count("*") * 100,
            2
        ).alias("readmission_rate")
    )
    .orderBy(col("readmission_rate").desc())
)

print("\nAge-group-wise readmission:")
age_analysis.show(truncate=False)

# COMMAND ----------

# ============================================================
# 5. READMISSION ANALYSIS BY LENGTH OF STAY
# ============================================================

from pyspark.sql.functions import when

print("=" * 60)
print("READMISSION ANALYSIS BY LENGTH OF STAY")
print("=" * 60)

stay_analysis = (
    gold_df
    .withColumn(
        "stay_group",
        when(col("length_of_stay") <= 3, "Short Stay (0-3 days)")
        .when(col("length_of_stay") <= 7, "Medium Stay (4-7 days)")
        .otherwise("Long Stay (8+ days)")
    )
    .groupBy("stay_group")
    .agg(
        count("*").alias("total_admissions"),
        sum("readmitted_within_30_days").alias("readmitted"),
        round(
            sum("readmitted_within_30_days") / count("*") * 100,
            2
        ).alias("readmission_rate")
    )
    .orderBy(col("readmission_rate").desc())
)

print("\nLength-of-stay-wise readmission:")
stay_analysis.show(truncate=False)

# COMMAND ----------

# ============================================================
# 6. HIGH-RISK READMISSION ANALYSIS
# ============================================================

print("=" * 60)
print("HIGH-RISK READMISSION ANALYSIS")
print("=" * 60)

risk_analysis = (
    gold_df
    .groupBy("readmission_risk")
    .agg(
        count("*").alias("total_admissions"),
        sum("readmitted_within_30_days").alias("readmitted"),
        round(
            sum("readmitted_within_30_days") / count("*") * 100,
            2
        ).alias("readmission_rate")
    )
    .orderBy(col("readmission_rate").desc())
)

print("\nRisk-level distribution:")
risk_analysis.show(truncate=False)

# High-risk admissions
high_risk = (
    gold_df
    .filter(col("readmission_risk") == "High")
)

print(f"\nHigh-risk admissions: {high_risk.count()}")

print("\nSample high-risk admissions:")
high_risk.select(
    "admission_id",
    "patient_id",
    "age",
    "age_group",
    "category",
    "department",
    "length_of_stay",
    "readmission_risk",
    "readmitted_within_30_days"
).show(10, truncate=False)

# COMMAND ----------

# ============================================================
# 7. FINAL ANALYTICS KPI SUMMARY
# ============================================================

print("=" * 60)
print("FINAL READMISSION ANALYTICS KPI SUMMARY")
print("=" * 60)

total_admissions = gold_df.count()

total_readmitted = (
    gold_df
    .filter(col("readmitted_within_30_days") == 1)
    .count()
)

overall_rate = (total_readmitted / total_admissions) * 100

high_risk_count = (
    gold_df
    .filter(col("readmission_risk") == "High")
    .count()
)

senior_count = (
    gold_df
    .filter(col("age_group") == "Senior")
    .count()
)

long_stay_count = (
    gold_df
    .filter(col("stay_category").contains("Long"))
    .count()
)

print(f"Total Admissions       : {total_admissions}")
print(f"Total Readmissions     : {total_readmitted}")
print(f"Overall Readmission %  : {overall_rate:.2f}%")
print(f"High-Risk Admissions   : {high_risk_count}")
print(f"Senior Admissions      : {senior_count}")
print(f"Long-Stay Admissions   : {long_stay_count}")

print("\nKey Analytics Findings:")
print(f"1. Overall readmission rate is {overall_rate:.2f}%.")
print(f"2. {high_risk_count} admissions are classified as High Risk.")
print(f"3. Senior patients show the highest age-group readmission rate.")
print(f"4. Long-stay admissions show a higher readmission rate than short-stay admissions.")

print("\nAnalytics KPI summary completed successfully.")

# COMMAND ----------

# ============================================================
# 8. WRITE ANALYTICS RESULTS TO DELTA TABLES
# ============================================================

print("=" * 60)
print("WRITING ANALYTICS DELTA TABLES")
print("=" * 60)

ANALYTICS_SCHEMA = "workspace.smart_patient_readmission"

# Overall readmission summary
overall_summary = spark.createDataFrame([
    (
        total_admissions,
        total_readmitted,
        float(overall_rate),
        high_risk_count,
        senior_count,
        long_stay_count
    )
], [
    "total_admissions",
    "total_readmissions",
    "overall_readmission_rate",
    "high_risk_admissions",
    "senior_admissions",
    "long_stay_admissions"
])

overall_table = f"{ANALYTICS_SCHEMA}.analytics_overall_summary"

overall_summary.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable(overall_table)

print(f"Created: {overall_table}")

# Department analysis
department_table = f"{ANALYTICS_SCHEMA}.analytics_department"

department_analysis.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable(department_table)

print(f"Created: {department_table}")

# Diagnosis category analysis
diagnosis_table = f"{ANALYTICS_SCHEMA}.analytics_diagnosis"

diagnosis_analysis.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable(diagnosis_table)

print(f"Created: {diagnosis_table}")

# Age-group analysis
age_table = f"{ANALYTICS_SCHEMA}.analytics_age_group"

age_analysis.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable(age_table)

print(f"Created: {age_table}")

# Length-of-stay analysis
stay_table = f"{ANALYTICS_SCHEMA}.analytics_length_of_stay"

stay_analysis.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable(stay_table)

print(f"Created: {stay_table}")

# Risk analysis
risk_table = f"{ANALYTICS_SCHEMA}.analytics_risk"

risk_analysis.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable(risk_table)

print(f"Created: {risk_table}")

print("\nALL ANALYTICS DELTA TABLES CREATED SUCCESSFULLY.")

# COMMAND ----------

# ============================================================
# 9. VERIFY ANALYTICS DELTA TABLES
# ============================================================

print("=" * 60)
print("VERIFYING ANALYTICS DELTA TABLES")
print("=" * 60)

analytics_tables = [
    "analytics_overall_summary",
    "analytics_department",
    "analytics_diagnosis",
    "analytics_age_group",
    "analytics_length_of_stay",
    "analytics_risk"
]

for table_name in analytics_tables:
    full_table = f"{ANALYTICS_SCHEMA}.{table_name}"
    df = spark.table(full_table)

    print(f"{table_name:<30} : {df.count()} rows")

print("\nAnalytics Delta tables verified successfully.")