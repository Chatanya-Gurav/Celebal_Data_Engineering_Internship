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

