# Smart Patient Readmission Risk Pipeline

A production-style batch data engineering project built with
**Databricks, PySpark, Delta Lake, and Unity Catalog**. The pipeline
follows the **Medallion Architecture (Bronze → Silver → Gold →
Analytics)** to transform synthetic hospital admission data into
actionable readmission-risk insights.

> **Note:** The project specification/document provided for the
> assignment was used as the design reference. This README reflects the
> implementation that was actually executed and verified in Databricks.

------------------------------------------------------------------------

## 🔗 Databricks Project

The complete project is available in the shared Databricks workspace
folder:

**Databricks Project:**\
https://dbc-c2470b3e-08ac.cloud.databricks.com/browse/folders/338870519238193?o=7474647916943129

The project contains the Bronze, Silver, Gold, Analytics,
transformation, and utility components used in the pipeline.

------------------------------------------------------------------------

## 📌 Project Overview

Hospitals generate large volumes of patient admission and discharge
data. This project demonstrates how a data engineering pipeline can
clean, transform, enrich, and aggregate hospital data to identify
readmission patterns and high-risk admissions.

### Key Questions Addressed

-   Which diagnosis categories have higher readmission rates?
-   Which age groups have higher readmission rates?
-   How does length of stay relate to readmission?
-   Which admissions are classified as high risk?
-   What are the overall readmission KPIs?
-   Which departments have the highest admission/readmission activity?

------------------------------------------------------------------------

## 🏗️ Architecture

``` text
                ┌──────────────────────┐
                │   Synthetic Source   │
                │   Hospital Data      │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │   BRONZE LAYER       │
                │ Raw / Generated Data │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │   SILVER LAYER       │
                │ Cleaning + Standard- │
                │ ization + Features   │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │    GOLD LAYER        │
                │ Business Aggregation │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │     ANALYTICS        │
                │ KPI + Risk Reporting │
                └──────────────────────┘
```

------------------------------------------------------------------------

## 🥉 Bronze Layer

The Bronze layer contains the generated hospital data in its raw form.

### Implemented Bronze Tables

  Table                   Verified Rows Description
  --------------------- --------------- ---------------------------------
  `patients_bronze`                 240 Patient demographic information
  `diagnoses_bronze`                 12 Diagnosis/category master data
  `admissions_bronze`               662 Hospital admission events

The Bronze data is generated in Databricks and stored as Delta tables.

------------------------------------------------------------------------

## 🥈 Silver Layer

The Silver layer cleans and standardizes the Bronze data before it is
used for analytical processing.

### Implemented Silver Tables

  ------------------------------------------------------------------------
  Table                                Verified Rows Description
  --------------------- ---------------------------- ---------------------
  `patients_silver`                              240 Cleaned patient
                                                     records

  `diagnoses_silver`                              12 Standardized
                                                     diagnosis records

  `admissions_silver`                            662 Cleaned and
                                                     standardized
                                                     admission records
  ------------------------------------------------------------------------

### Silver Transformations

The pipeline performs operations including:

-   Data type standardization
-   String trimming
-   Case normalization
-   Date conversion
-   Length-of-stay conversion
-   Readmission flag conversion
-   Duplicate removal
-   Patient/diagnosis/admission preparation for downstream
    transformations

All three Silver Delta tables were successfully created and verified in
Databricks.

------------------------------------------------------------------------

## 🧩 Feature Engineering

A reusable PySpark module is maintained in:

``` text
transformations/
└── feature_engineering.py
```

### Engineered Features

#### Age Group

Patients are categorized into:

  Age       Category
  --------- -------------
  `< 18`    Pediatric
  `18–35`   Young Adult
  `36–60`   Middle Age
  `> 60`    Senior

#### Length-of-Stay Category

Admissions are grouped into:

-   Short Stay: 0--3 days
-   Medium Stay: 4--7 days
-   Long Stay: 8+ days

#### Readmission Risk

``` text
Readmitted within 30 days = High
Otherwise                  = Low
```

The feature-engineering functions are designed as reusable PySpark
DataFrame transformations.

------------------------------------------------------------------------

## 🥇 Gold Layer

The Gold layer converts cleaned data into business-oriented analytical
outputs.

The implementation creates aggregated Delta tables for:

-   Overall admission/readmission summary
-   Department-level analysis
-   Diagnosis-category analysis
-   Age-group analysis
-   Length-of-stay analysis
-   Readmission-risk distribution

These tables are used by the Analytics layer for reporting and KPI
generation.

------------------------------------------------------------------------

## 📊 Analytics & KPI Results

The executed Databricks analytics produced the following verified
results.

### Overall KPI Summary

  KPI                          Result
  -------------------------- --------
  Total Admissions                662
  Total Readmissions              149
  Overall Readmission Rate     22.51%
  High-Risk Admissions            149
  Senior Admissions               293
  Long-Stay Admissions            320

### Key Findings

1.  The overall readmission rate is **22.51%**.
2.  **149 admissions** are classified as High Risk.
3.  **Senior patients** have the highest readmission rate among the age
    groups.
4.  Long-stay admissions show a higher readmission rate than short-stay
    admissions.

------------------------------------------------------------------------

## 🏥 Diagnosis Category Analysis

The executed analytics identified the following readmission rates:

  ---------------------------------------------------------------------------
  Diagnosis Category   Total Admissions         Readmitted   Readmission Rate
  ------------------ ------------------ ------------------ ------------------
  Oncology                           97                 27             27.84%

  Cardiovascular                    151                 39             25.83%

  Respiratory                       115                 28             24.35%

  Infectious                         48                 11             22.92%

  Renal                              40                  9             22.50%

  Neurological                       52                  9             17.31%

  Endocrine                          52                  9             17.31%

  Orthopedic                         70                 12             17.14%

  Gastrointestinal                   37                  5             13.51%
  ---------------------------------------------------------------------------

**Observation:** Oncology and Cardiovascular admissions have the highest
observed readmission rates in the executed dataset.

------------------------------------------------------------------------

## 👥 Age Group Analysis

  Age Group       Total Admissions   Readmitted   Readmission Rate
  ------------- ------------------ ------------ ------------------
  Senior                       293           95             32.42%
  Pediatric                     13            3             23.08%
  Middle Age                   213           35             16.43%
  Young Adult                  143           16             11.19%

**Observation:** Senior patients have the highest observed readmission
rate at **32.42%**.

------------------------------------------------------------------------

## 🛏️ Length-of-Stay Analysis

  Stay Group                  Total Admissions   Readmitted   Readmission Rate
  ------------------------- ------------------ ------------ ------------------
  Long Stay (8+ days)                      320           80             25.00%
  Medium Stay (4--7 days)                  296           65             21.96%
  Short Stay (0--3 days)                    46            4              8.70%

**Observation:** Long-stay admissions have the highest observed
readmission rate among the three stay categories.

------------------------------------------------------------------------

## 🚨 High-Risk Readmission Analysis

The executed risk analysis produced:

  Risk Level     Total Admissions   Readmitted   Readmission Rate
  ------------ ------------------ ------------ ------------------
  High                        149          149             100.0%
  Low                         513            0               0.0%

A total of **149 admissions** were classified as High Risk.

Sample high-risk records included patients across Oncology, Respiratory,
Cardiovascular, and Neurological categories and across different
departments.

------------------------------------------------------------------------

## ⚡ Spark & Delta Lake Practices

The project uses PySpark and Delta Lake features suitable for
production-style data engineering workflows.

### Spark Optimization

The project design includes:

-   Adaptive Query Execution (AQE)
-   Adaptive partition coalescing
-   Skew join handling
-   Broadcast joins for small dimension tables
-   Controlled shuffle partition configuration
-   Explicit partitioning for window-based processing

### Delta Lake

The pipeline uses:

-   Delta table format
-   Overwrite-based idempotent processing
-   Schema management
-   `OPTIMIZE`
-   `ZORDER`
-   `ANALYZE TABLE`
-   Post-write table verification

------------------------------------------------------------------------

## 🗂️ Project Structure

``` text
Smart-Patient-Readmission-Risk-Pipeline/
│
├── README.md
├── config.py
│
├── utils/
│   └── helpers.py
│
├── transformations/
│   └── feature_engineering.py
│
├── bronze/
│   └── generate_data
│
├── silver/
│   └── silver_transformations
│
├── gold/
│   └── gold_transformations
│
└── analytics/
    └── sql_analytics 
```

### Module Responsibilities

  ------------------------------------------------------------------------------
  Module                                     Responsibility
  ------------------------------------------ -----------------------------------
  `config.py`                                Central configuration for catalog,
                                             schema, tables, and Spark settings

  `utils/helpers.py`                         Reusable validation, data-quality,
                                             and optimization utilities

  `transformations/feature_engineering.py`   Reusable PySpark
                                             feature-engineering functions

  `bronze/generate_data`                     Generates synthetic patient,
                                             diagnosis, and admission data

  `silver/silver_transformations`            Cleans and standardizes Bronze data

  `gold/gold_transformations`                Creates business-level analytical
                                             transformations

  `analytics/analytics_report`               Generates KPI and readmission-risk
                                             reports
  ------------------------------------------------------------------------------

------------------------------------------------------------------------

## 🧱 Unity Catalog

The executed project uses:

``` text
Catalog : workspace
Schema  : smart_patient_readmission
```

### Verified Tables

``` text
workspace.smart_patient_readmission.patients_bronze
workspace.smart_patient_readmission.diagnoses_bronze
workspace.smart_patient_readmission.admissions_bronze

workspace.smart_patient_readmission.patients_silver
workspace.smart_patient_readmission.diagnoses_silver
workspace.smart_patient_readmission.admissions_silver
```

Analytics Delta tables were also created and verified successfully under
the same schema.

------------------------------------------------------------------------

## ▶️ Execution Order

Run the project in the following order:

``` text
1. bronze/generate_data
        ↓
2. silver/silver_transformations
        ↓
3. transformations/feature_engineering.py
        ↓
4. gold/gold_transformations
        ↓
5. analytics/analytics_report
```

The executed notebooks successfully produced and verified the required
Delta tables and analytical outputs.

------------------------------------------------------------------------

## 🔍 Data Validation

Validation was performed at different stages of the pipeline, including:

-   Row-count verification
-   Duplicate handling
-   Data-type standardization
-   Delta table verification
-   Analytical result validation
-   Risk-level distribution checks

The final analytics verification confirmed:

``` text
analytics_overall_summary : 1 row
analytics_department      : 11 rows
analytics_diagnosis       : 9 rows
analytics_age_group       : 4 rows
analytics_length_of_stay : 3 rows
analytics_risk            : 2 rows
```

------------------------------------------------------------------------

## 💼 Business Value

This pipeline demonstrates how hospital data can be transformed into
actionable insights for:

-   Clinical risk identification
-   Patient follow-up prioritization
-   Department performance analysis
-   Diagnosis-specific care planning
-   Hospital capacity planning
-   Readmission monitoring
-   Operational decision-making

------------------------------------------------------------------------

## 🚀 Future Enhancements

Possible future improvements include:

1.  Real-time ingestion using Databricks Auto Loader
2.  Machine-learning-based readmission prediction
3.  Incremental processing using `MERGE INTO`
4.  AI/BI dashboard development
5.  Automated data-quality expectations
6.  Alerting for high-risk admission thresholds
7.  Databricks Asset Bundles for CI/CD
8.  Incremental patient risk scoring

------------------------------------------------------------------------

## 🛠️ Technologies Used

-   **Databricks**
-   **Apache Spark / PySpark**
-   **Delta Lake**
-   **Unity Catalog**
-   **Python**
-   **SQL**
-   **Medallion Architecture**
-   **Spark DataFrame API**

------------------------------------------------------------------------

## ✅ Project Status

**Status: Completed and Verified**

The complete pipeline was executed in Databricks, including:

-   Bronze data generation
-   Silver cleaning and standardization
-   Feature engineering
-   Gold transformations
-   Analytics/KPI reporting
-   High-risk readmission analysis
-   Delta table creation
-   Delta table verification
