from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def add_age_group(df: DataFrame) -> DataFrame:
    """
    Add age_group based on patient age.

    Categories:
    - Pediatric: age < 18
    - Young Adult: 18-35
    - Middle Age: 36-60
    - Senior: > 60
    """

    return df.withColumn(
        "age_group",
        F.when(F.col("age") < 18, "Pediatric")
         .when(F.col("age").between(18, 35), "Young Adult")
         .when(F.col("age").between(36, 60), "Middle Age")
         .otherwise("Senior")
    )


def add_stay_category(df: DataFrame) -> DataFrame:
    """
    Add stay_category based on length_of_stay.

    Categories:
    - Short Stay: 0-3 days
    - Medium Stay: 4-7 days
    - Long Stay: 8+ days
    """

    return df.withColumn(
        "stay_category",
        F.when(F.col("length_of_stay") <= 3, "Short Stay (0-3 days)")
         .when(F.col("length_of_stay").between(4, 7), "Medium Stay (4-7 days)")
         .otherwise("Long Stay (8+ days)")
    )


def add_readmission_risk(df: DataFrame) -> DataFrame:
    """
    Add readmission_risk based on readmission within 30 days.

    - High: readmitted within 30 days
    - Low: not readmitted within 30 days
    """

    return df.withColumn(
        "readmission_risk",
        F.when(
            F.col("readmitted_within_30_days") == 1,
            "High"
        ).otherwise("Low")
    )


def engineer_features(df: DataFrame) -> DataFrame:
    """
    Apply all feature-engineering transformations.
    """

    df = add_age_group(df)
    df = add_stay_category(df)
    df = add_readmission_risk(df)

    return df