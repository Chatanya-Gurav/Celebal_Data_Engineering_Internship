# Celebal_Data_Engineering_Internship

This repository contains all weekly assignments completed during the Celebal Technologies Data Engineering Internship.

---

## Repository Structure

```text
Celebal_Data_Engineering_Internship/
│
├── Week_1/
├── Week_2/
├── Week_3/
├── Week_4/
├── Week_5/
├── Week_6/
├── Week_7/
├── Week_8/
└── README.md
```

---

## Assignment Index

| Week | Assignment | Status |
|------|------------|--------|
| Week 1 | Data Exploration and Cleaning using Pandas | ✅ Completed |
| Week 2 | SQL Basics | ⏳ Upcoming |
| Week 3 | Subqueries | ⏳ Upcoming |
| Week 4 | Data Engineering Concepts | ⏳ Upcoming |
| Week 5 | Data Cleaning | ⏳ Upcoming |
| Week 6 | Spark Intro | ⏳ Upcoming |
| Week 7 | Databricks | ⏳ Upcoming |
| Week 8 | planning | ⏳ Upcoming |


----------------------------------------------------------------------------------------
# WEEK1 ASSIGNMENT

# Data Exploration and Cleaning using Pandas

## Objective

The objective of this project is to perform basic data exploration and cleaning using Python and Pandas on the `Combined_dataset.csv` shopping dataset.

## Dataset

- Source: https://www.kaggle.com/datasets/anvitkumar/shopping-dataset
- File used: `Combined_dataset.csv`

## Tasks Performed

- Loaded the dataset into a Pandas DataFrame
- Explored the data using `head()`, `tail()`, `shape`, `info()`, and `describe()`
- Identified and handled missing values
- Filtered rows and selected relevant columns
- Removed duplicate records
- Converted the `final_price` column to numeric format
- Created a derived column: `total_amount`
- Saved the cleaned dataset as `Combined_dataset_cleaned.csv`

## Note

The original dataset does not contain a `quantity` column. Therefore, `ratings_count` was used as a proxy variable to create the `total_amount` column.

## Technologies Used

- Python
- Pandas
- NumPy
- Jupyter Notebook
- Visual Studio Code

## Files Included

- `Data_Exploration_Cleaning.ipynb`
- `Combined_dataset.csv`
- `Combined_dataset_cleaned.csv`

## Output

A cleaned version of the dataset was generated and saved as `Combined_dataset_cleaned.csv`.

------------------------------------------------------------------------------------------
