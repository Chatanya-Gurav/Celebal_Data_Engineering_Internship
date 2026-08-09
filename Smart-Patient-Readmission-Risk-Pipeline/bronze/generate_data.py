# Databricks notebook source
import sys

sys.path.append("..")

import config as cfg

print("CONFIG TEST")
print("=" * 50)

print("Catalog :", cfg.CATALOG)
print("Schema  :", cfg.SCHEMA)

print("\nBronze tables:")
print(cfg.BRONZE_PATIENTS)
print(cfg.BRONZE_DIAGNOSES)
print(cfg.BRONZE_ADMISSIONS)

print("\nConfiguration loaded successfully.")

# COMMAND ----------

# ============================================================
# BRONZE LAYER - IMPORTS AND CONFIGURATION
# ============================================================

import sys
import importlib

# Add project root so config.py and utils/ are available
sys.path.append("..")

# Reload project modules
for mod_name in list(sys.modules.keys()):
    if mod_name in (
        "config",
        "utils",
        "utils.helpers",
    ):
        del sys.modules[mod_name]

importlib.invalidate_caches()

from datetime import date, timedelta
import random

from pyspark.sql import functions as F
from pyspark.sql import types as T

import config as cfg

from utils.helpers import (
    apply_spark_optimizations,
    optimize_table,
    analyze_table,
    inject_nulls,
    inject_inconsistent_categories,
    inject_date_noise,
    weighted_choice,
    generate_phone,
    log_table_stats,
    validate_no_duplicates,
    write_delta_overwrite,
)

# Reproducibility
random.seed(cfg.RANDOM_SEED)

# Apply Spark optimizations
apply_spark_optimizations(
    spark,
    cfg.SPARK_OPTIMIZATIONS
)

# Ensure project schema exists
spark.sql(
    f"CREATE SCHEMA IF NOT EXISTS "
    f"{cfg.CATALOG}.{cfg.SCHEMA}"
)

print("=" * 60)
print("BRONZE LAYER INITIALIZED")
print("=" * 60)
print(f"Catalog : {cfg.CATALOG}")
print(f"Schema  : {cfg.SCHEMA}")
print("Ready for synthetic data generation.")

# COMMAND ----------

# ============================================================
# BRONZE LAYER - PROJECT-COMPATIBLE DATA GENERATION
# ============================================================

import random
from datetime import date, timedelta

from pyspark.sql import functions as F
from pyspark.sql import types as T

from utils.helpers import (
    inject_nulls,
    inject_inconsistent_categories,
    inject_date_noise,
    weighted_choice,
    generate_phone
)

random.seed(cfg.RANDOM_SEED)

print("=" * 60)
print("GENERATING PROJECT BRONZE DATA")
print("=" * 60)


# ============================================================
# 1. PATIENTS
# ============================================================

FIRST_NAMES_M = [
    "Rahul", "Amit", "Vikram", "Suresh", "Rajesh",
    "Arjun", "Kiran", "Manoj", "Deepak", "Sanjay",
    "Anil", "Ravi", "Nitin", "Pankaj", "Gaurav"
]

FIRST_NAMES_F = [
    "Priya", "Anita", "Sunita", "Kavita", "Neha",
    "Pooja", "Meera", "Swati", "Asha", "Rekha",
    "Divya", "Nisha", "Ritu", "Seema", "Jyoti"
]

LAST_NAMES = [
    "Sharma", "Patel", "Singh", "Kumar", "Gupta",
    "Reddy", "Mehta", "Verma", "Joshi", "Nair",
    "Das", "Roy", "Sen", "Rao", "Kulkarni"
]

num_patients = random.randint(*cfg.NUM_PATIENTS)

patients = []

for i in range(1, num_patients + 1):

    age_bucket = random.random()

    if age_bucket < 0.05:
        age = random.randint(1, 18)
    elif age_bucket < 0.20:
        age = random.randint(19, 35)
    elif age_bucket < 0.55:
        age = random.randint(36, 60)
    elif age_bucket < 0.85:
        age = random.randint(61, 79)
    else:
        age = random.randint(80, 95)

    gender = random.choices(
        ["F", "M", "Other"],
        weights=[0.49, 0.49, 0.02],
        k=1
    )[0]

    if gender == "F":
        first = random.choice(FIRST_NAMES_F)
    else:
        first = random.choice(FIRST_NAMES_M)

    last = random.choice(LAST_NAMES)

    name = f"{first} {last}"
    contact = generate_phone()

    patients.append([
        f"P{str(i).zfill(5)}",
        name,
        age,
        gender,
        contact
    ])

print(f"Generated {len(patients)} patients")


# ============================================================
# 2. DIAGNOSES
# ============================================================

diagnosis_rows = list(cfg.DIAGNOSIS_CATALOG)

diagnoses_by_id = {
    d[0]: {
        "icd_code": d[1],
        "category": d[2]
    }
    for d in diagnosis_rows
}

diag_ids = [d[0] for d in diagnosis_rows]

print(f"Generated {len(diagnosis_rows)} diagnoses")


# ============================================================
# 3. ADMISSIONS
# ============================================================

num_admissions = random.randint(*cfg.NUM_ADMISSIONS)

start_date = date.today() - timedelta(
    days=cfg.DATA_WINDOW_DAYS
)

patients_by_id = {
    p[0]: {
        "age": p[2],
        "gender": p[3]
    }
    for p in patients
}

admissions = []

for i in range(1, num_admissions + 1):

    admission_id = f"A{str(i).zfill(6)}"

    patient_id = random.choice(patients)[0]

    diagnosis_id = random.choices(
        diag_ids,
        weights=cfg.DIAGNOSIS_WEIGHTS,
        k=1
    )[0]

    age = patients_by_id[patient_id]["age"]

    category = diagnoses_by_id[diagnosis_id]["category"]

    department = weighted_choice(
        cfg.CATEGORY_DEPARTMENT_MAP[category]
    )

    physician = random.choice(
        cfg.PHYSICIANS.get(
            department,
            ["Dr. Unknown"]
        )
    )

    admission_date = (
        start_date
        + timedelta(
            days=random.randint(
                0,
                cfg.DATA_WINDOW_DAYS - 1
            )
        )
    )

    los_range = cfg.BASE_LOS_RANGES.get(
        department,
        (1, 6)
    )

    base_los = random.randint(*los_range)

    age_modifier = (
        2 if age >= 80
        else 1 if age >= 65
        else 0
    )

    category_modifier = (
        2
        if category in (
            "Cardiovascular",
            "Oncology",
            "Infectious"
        )
        else 0
    )

    length_of_stay = max(
        1,
        base_los
        + age_modifier
        + category_modifier
        + random.randint(-1, 2)
    )

    discharge_date = (
        admission_date
        + timedelta(days=length_of_stay)
    )

    # Readmission probability
    if age >= 80:
        readmit_prob = 0.34
    elif age >= 65:
        readmit_prob = 0.26
    elif age >= 50:
        readmit_prob = 0.18
    else:
        readmit_prob = 0.10

    if category in (
        "Cardiovascular",
        "Respiratory",
        "Oncology"
    ):
        readmit_prob += 0.06

    if department in (
        "General Medicine",
        "ICU"
    ):
        readmit_prob += 0.04

    readmitted_within_30_days = (
        1
        if random.random()
        < min(readmit_prob, 0.55)
        else 0
    )

    admissions.append([
        admission_id,
        patient_id,
        diagnosis_id,
        department,
        physician,
        admission_date.isoformat(),
        discharge_date.isoformat(),
        length_of_stay,
        readmitted_within_30_days
    ])

print(f"Generated {len(admissions)} admissions")


# ============================================================
# 4. DATA QUALITY INJECTION
# ============================================================

# Patients: 5% nulls in name and contact
patients = inject_nulls(
    patients,
    col_indices=[1, 4],
    rate=cfg.NULL_INJECTION_RATE
)

# Admissions: 5% nulls in physician and LOS
admissions = inject_nulls(
    admissions,
    col_indices=[4, 7],
    rate=cfg.NULL_INJECTION_RATE
)

# Inconsistent department values
dept_noise = {
    "Cardiology": [
        "cardiology",
        "CARDIOLOGY",
        "Cardio"
    ],
    "General Medicine": [
        "general medicine",
        "Gen Medicine",
        "Gen. Medicine"
    ],
    "Orthopedics": [
        "orthopedics",
        "ORTHOPEDICS",
        "Ortho"
    ],
    "Neurology": [
        "neurology",
        "NEUROLOGY",
        "Neuro"
    ],
    "Oncology": [
        "oncology",
        "ONCOLOGY",
        "Onco"
    ],
    "Pulmonology": [
        "pulmonology",
        "Pulmo"
    ],
    "ICU": [
        "icu"
    ]
}

admissions = inject_inconsistent_categories(
    admissions,
    col_idx=3,
    valid_values=cfg.DEPARTMENTS,
    noise_map=dept_noise,
    rate=cfg.INCONSISTENT_CATEGORY_RATE
)

# 2% discharge-date noise
admissions = inject_date_noise(
    admissions,
    col_idx=6,
    max_jitter_days=cfg.DATE_NOISE_DAYS,
    rate=0.02
)

print("Data quality injection complete")


# ============================================================
# 5. CREATE DATAFRAMES WITH REQUIRED SCHEMAS
# ============================================================

patients_schema = T.StructType([
    T.StructField(
        "patient_id",
        T.StringType(),
        False
    ),
    T.StructField(
        "name",
        T.StringType(),
        True
    ),
    T.StructField(
        "age",
        T.IntegerType(),
        True
    ),
    T.StructField(
        "gender",
        T.StringType(),
        True
    ),
    T.StructField(
        "contact",
        T.StringType(),
        True
    )
])

diagnoses_schema = T.StructType([
    T.StructField(
        "diagnosis_id",
        T.StringType(),
        False
    ),
    T.StructField(
        "icd_code",
        T.StringType(),
        False
    ),
    T.StructField(
        "category",
        T.StringType(),
        False
    )
])

admissions_schema = T.StructType([
    T.StructField(
        "admission_id",
        T.StringType(),
        False
    ),
    T.StructField(
        "patient_id",
        T.StringType(),
        False
    ),
    T.StructField(
        "diagnosis_id",
        T.StringType(),
        False
    ),
    T.StructField(
        "department",
        T.StringType(),
        True
    ),
    T.StructField(
        "physician",
        T.StringType(),
        True
    ),
    T.StructField(
        "admission_date",
        T.StringType(),
        True
    ),
    T.StructField(
        "discharge_date",
        T.StringType(),
        True
    ),
    T.StructField(
        "length_of_stay",
        T.IntegerType(),
        True
    ),
    T.StructField(
        "readmitted_within_30_days",
        T.IntegerType(),
        True
    )
])

patients_df = spark.createDataFrame(
    patients,
    schema=patients_schema
)

diagnoses_df = spark.createDataFrame(
    diagnosis_rows,
    schema=diagnoses_schema
)

admissions_df = (
    spark.createDataFrame(
        admissions,
        schema=admissions_schema
    )
    .withColumn(
        "admission_date",
        F.to_date("admission_date")
    )
    .withColumn(
        "discharge_date",
        F.to_date("discharge_date")
    )
)


# ============================================================
# FINAL CHECK
# ============================================================

print("=" * 60)
print("BRONZE DATAFRAMES READY")
print("=" * 60)

print(
    f"patients_df   : {patients_df.count()} rows, "
    f"{len(patients_df.columns)} columns"
)

print(
    f"diagnoses_df  : {diagnoses_df.count()} rows, "
    f"{len(diagnoses_df.columns)} columns"
)

print(
    f"admissions_df : {admissions_df.count()} rows, "
    f"{len(admissions_df.columns)} columns"
)

print("\nPatients schema:")
patients_df.printSchema()

print("\nDiagnoses schema:")
diagnoses_df.printSchema()

print("\nAdmissions schema:")
admissions_df.printSchema()

print("=" * 60)
print("BRONZE GENERATION COMPLETE")
print("=" * 60)

# COMMAND ----------

# ============================================================
# WRITE BRONZE DATA TO DELTA TABLES
# ============================================================

print("=" * 60)
print("WRITING BRONZE DELTA TABLES")
print("=" * 60)

# Patients
(
    patients_df
    .write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(cfg.BRONZE_PATIENTS)
)

print(f"Created: {cfg.BRONZE_PATIENTS}")


# Diagnoses
(
    diagnoses_df
    .write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(cfg.BRONZE_DIAGNOSES)
)

print(f"Created: {cfg.BRONZE_DIAGNOSES}")


# Admissions
(
    admissions_df
    .write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(cfg.BRONZE_ADMISSIONS)
)

print(f"Created: {cfg.BRONZE_ADMISSIONS}")


print("=" * 60)
print("BRONZE DELTA TABLES CREATED SUCCESSFULLY")
print("=" * 60)