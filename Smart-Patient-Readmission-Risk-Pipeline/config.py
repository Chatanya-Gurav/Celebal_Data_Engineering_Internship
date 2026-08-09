# Smart Patient Readmission Risk Pipeline
# Central project configuration

# ============================================================
# UNITY CATALOG
# ============================================================

CATALOG = "workspace"
SCHEMA = "smart_patient_readmission"

SCHEMA_FULL_NAME = f"{CATALOG}.{SCHEMA}"


# ============================================================
# DELTA TABLE NAMES
# ============================================================

BRONZE_PATIENTS = f"{SCHEMA_FULL_NAME}.patients_bronze"
BRONZE_DIAGNOSES = f"{SCHEMA_FULL_NAME}.diagnoses_bronze"
BRONZE_ADMISSIONS = f"{SCHEMA_FULL_NAME}.admissions_bronze"

SILVER_ADMISSIONS = f"{SCHEMA_FULL_NAME}.silver_admissions_enriched"

GOLD_READMISSION_BY_DIAGNOSIS = (
    f"{SCHEMA_FULL_NAME}.readmission_by_diagnosis"
)

GOLD_DEPARTMENT_PERFORMANCE = (
    f"{SCHEMA_FULL_NAME}.department_performance"
)

GOLD_AGE_GROUP_RISK = (
    f"{SCHEMA_FULL_NAME}.age_group_risk"
)

GOLD_PATIENT_RISK_PROFILE = (
    f"{SCHEMA_FULL_NAME}.patient_risk_profile"
)


# Aliases used by some project code
PATIENTS_BRONZE = BRONZE_PATIENTS
DIAGNOSES_BRONZE = BRONZE_DIAGNOSES
ADMISSIONS_BRONZE = BRONZE_ADMISSIONS

SILVER_TABLE = SILVER_ADMISSIONS

READMISSION_BY_DIAGNOSIS = GOLD_READMISSION_BY_DIAGNOSIS
DEPARTMENT_PERFORMANCE = GOLD_DEPARTMENT_PERFORMANCE
AGE_GROUP_RISK = GOLD_AGE_GROUP_RISK
PATIENT_RISK_PROFILE = GOLD_PATIENT_RISK_PROFILE


# ============================================================
# DATA GENERATION
# ============================================================

RANDOM_SEED = 42

# Project requirement: 200–250 patients
NUM_PATIENTS = (200, 250)

# Project requirement: 500–700 admissions
NUM_ADMISSIONS = (500, 700)

# One year of synthetic admission history
DATA_WINDOW_DAYS = 365


# ============================================================
# DATA QUALITY SIMULATION
# ============================================================

# Project requirement: 5% null injection
NULL_INJECTION_RATE = 0.05

# Project requirement: 3% inconsistent categorical values
INCONSISTENT_CATEGORY_RATE = 0.03

# Project requirement: +/- 2 days discharge-date noise
DATE_NOISE_DAYS = 2


# ============================================================
# DEPARTMENTS
# ============================================================

DEPARTMENTS = [
    "Cardiology",
    "General Medicine",
    "Orthopedics",
    "Neurology",
    "Oncology",
    "Pulmonology",
    "ICU",
]


# ============================================================
# DIAGNOSIS MASTER DATA
# 12 ICD-10-style diagnosis records
# ============================================================

DIAGNOSIS_CATALOG = [
    ("D001", "I25.10", "Cardiovascular"),
    ("D002", "I50.9", "Cardiovascular"),
    ("D003", "J18.9", "Respiratory"),
    ("D004", "J44.9", "Respiratory"),
    ("D005", "C50.9", "Oncology"),
    ("D006", "C34.90", "Oncology"),
    ("D007", "M17.9", "Orthopedic"),
    ("D008", "G40.909", "Neurological"),
    ("D009", "A41.9", "Infectious"),
    ("D010", "E11.9", "Endocrine"),
    ("D011", "K21.9", "Gastrointestinal"),
    ("D012", "N18.9", "Renal"),
]

# Weights correspond one-to-one with DIAGNOSIS_CATALOG.
DIAGNOSIS_WEIGHTS = [
    12,  # D001
    10,  # D002
    11,  # D003
    8,   # D004
    9,   # D005
    6,   # D006
    9,   # D007
    8,   # D008
    7,   # D009
    8,   # D010
    6,   # D011
    6,   # D012
]


# ============================================================
# DIAGNOSIS → DEPARTMENT DISTRIBUTION
# ============================================================

CATEGORY_DEPARTMENT_MAP = {

    "Cardiovascular": [
        ("Cardiology", 72),
        ("ICU", 20),
        ("General Medicine", 8),
    ],

    "Respiratory": [
        ("Pulmonology", 70),
        ("General Medicine", 20),
        ("ICU", 10),
    ],

    "Oncology": [
        ("Oncology", 75),
        ("General Medicine", 15),
        ("ICU", 10),
    ],

    "Orthopedic": [
        ("Orthopedics", 85),
        ("General Medicine", 15),
    ],

    "Neurological": [
        ("Neurology", 80),
        ("ICU", 10),
        ("General Medicine", 10),
    ],

    "Infectious": [
        ("General Medicine", 65),
        ("ICU", 25),
        ("Pulmonology", 10),
    ],

    "Endocrine": [
        ("General Medicine", 80),
        ("Cardiology", 10),
        ("ICU", 10),
    ],

    "Gastrointestinal": [
        ("General Medicine", 75),
        ("ICU", 10),
        ("Oncology", 15),
    ],

    "Renal": [
        ("General Medicine", 70),
        ("ICU", 20),
        ("Cardiology", 10),
    ],
}


# ============================================================
# PHYSICIAN ROSTER
# ============================================================

PHYSICIANS = {
    "Cardiology": [
        "Dr. Mehta",
        "Dr. Rao",
        "Dr. Shah",
    ],

    "General Medicine": [
        "Dr. Patil",
        "Dr. Kulkarni",
        "Dr. Deshmukh",
    ],

    "Orthopedics": [
        "Dr. Joshi",
        "Dr. Sharma",
        "Dr. Verma",
    ],

    "Neurology": [
        "Dr. Iyer",
        "Dr. Nair",
        "Dr. Singh",
    ],

    "Oncology": [
        "Dr. Kapoor",
        "Dr. Gupta",
        "Dr. Reddy",
    ],

    "Pulmonology": [
        "Dr. Rao",
        "Dr. Menon",
        "Dr. Bhat",
    ],

    "ICU": [
        "Dr. Kumar",
        "Dr. Mishra",
        "Dr. Sinha",
    ],
}


# ============================================================
# BASE LENGTH-OF-STAY RANGES
# ============================================================

BASE_LOS_RANGES = {
    "Cardiology": (3, 8),
    "General Medicine": (2, 6),
    "Orthopedics": (3, 7),
    "Neurology": (3, 8),
    "Oncology": (4, 10),
    "Pulmonology": (3, 8),
    "ICU": (5, 12),
}


# ============================================================
# SPARK OPTIMIZATION SETTINGS
# Based on project specification
# ============================================================

SPARK_OPTIMIZATIONS = {
    "spark.sql.adaptive.enabled": "true",
    "spark.sql.adaptive.coalescePartitions.enabled": "true",
    "spark.sql.adaptive.skewJoin.enabled": "true",
    "spark.sql.adaptive.skewJoin.skewedPartitionFactor": "5",
    "spark.sql.adaptive.advisoryPartitionSizeInBytes": "128m",
    "spark.sql.autoBroadcastJoinThreshold": str(10 * 1024 * 1024),
    "spark.sql.shuffle.partitions": "200",
}


# ============================================================
# ZORDER CONFIGURATION
# ============================================================

ZORDER_COLUMNS = {
    BRONZE_ADMISSIONS: ["patient_id", "admission_date"],

    SILVER_ADMISSIONS: [
        "patient_id",
        "admission_date",
        "department",
    ],

    GOLD_READMISSION_BY_DIAGNOSIS: [
        "diagnosis_category",
    ],

    GOLD_DEPARTMENT_PERFORMANCE: [
        "department",
    ],

    GOLD_PATIENT_RISK_PROFILE: [
        "patient_id",
        "risk_category",
    ],
}