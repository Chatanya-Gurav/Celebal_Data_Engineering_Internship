# E-Commerce Order Analytics System

## 1. Project Overview

The E-Commerce Order Analytics System is an end-to-end data analytics project built using Python and SQL.

The project generates realistic e-commerce datasets, introduces intentional data inconsistencies, cleans and validates the data using Pandas, loads the cleaned data into a SQLite database, and performs business analytics using SQL.

The system also includes a Python command-line reporting tool and edge-case testing to ensure reliable and consistent results.

---

## 2. Objective

The main objective of this project is to design and develop an end-to-end e-commerce analytics system covering:

- Data generation
- Data cleaning and validation
- Referential integrity checking
- Relational database loading
- SQL analytics
- Window functions
- CTEs
- Cohort and retention analysis
- Customer segmentation
- Command-line reporting
- Edge-case testing
- Business reporting

---

## 3. Technologies Used

- Python 3.13
- Pandas
- Faker
- SQLite
- SQL
- CSV
- Git & GitHub
- VS Code

---

## 4. Project Architecture

```text
Raw CSV Data
     |
     v
Data Generation
(generate_data.py)
     |
     v
Data Cleaning & Validation
(clean_data.py)
     |
     v
Cleaned CSV Data
     |
     v
SQLite Database
(load_database.py)
     |
     +-----------------------+
     |                       |
     v                       v
SQL Analytics           Python CLI
     |                  Reporting Tool
     |                  (report_cli.py)
     v                       |
Business Insights <----------+
     |
     v
Sample Reports