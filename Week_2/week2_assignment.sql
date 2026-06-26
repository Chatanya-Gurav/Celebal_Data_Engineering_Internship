/*=============================================================
                CELEBAL TECHNOLOGIES

            Data Engineering Internship
                  Week 2 Assignment

      Project : SQL-Based Data Analysis
      Dataset : Sample Superstore
      Database: week2_assignment

      Name    : Chaitanya Gurav

=============================================================*/

CREATE DATABASE week2_assignment;

USE week2_assignment;

/*=============================================================
                SECTION 1
            DATASET EXPLORATION
=============================================================*/

-- Query 1 : Count Total Records

SELECT COUNT(*) AS Total_Rows
FROM superstore;

-- Query 2 : Display Sample Records

SELECT *
FROM superstore
LIMIT 10;

-- Query 3 : Display Table Structure

DESCRIBE superstore;

/*=============================================================
                SECTION 2
               WHERE CLAUSE
=============================================================*/

-- Query 4: Display all orders from the West Region

SELECT *
FROM superstore
WHERE Region = 'West';
---------------------------------------------------------------
-- Query 5: Display all Furniture category orders

SELECT *
FROM superstore
WHERE Category = 'Furniture';
--------------------------------------------------------------
-- Query 6: Display orders with Sales greater than 500

SELECT *
FROM superstore
WHERE Sales > 500;
---------------------------------------------------------------
-- Query 7: Display orders with Profit greater than 100

SELECT *
FROM superstore
WHERE Profit > 100;
---------------------------------------------------------------
-- Query 8: Display orders with Discount greater than 20%

SELECT *
FROM superstore
WHERE Discount > 0.20;
---------------------------------------------------------------
-- Query 9: Display orders with Quantity greater than or equal to 5

SELECT *
FROM superstore
WHERE Quantity >= 5;
---------------------------------------------------------------
-- Query 10: Display all orders from California

SELECT *
FROM superstore
WHERE State = 'California';
---------------------------------------------------------------
-- Query 11: Display all orders from New York City

SELECT *
FROM superstore
WHERE City = 'New York City';
---------------------------------------------------------------
-- Query 12: Display Technology products sold in the West Region

SELECT *
FROM superstore
WHERE Category = 'Technology'
AND Region = 'West';
---------------------------------------------------------------
-- Query 13: Display orders where Sales are between 100 and 500

SELECT *
FROM superstore
WHERE Sales BETWEEN 100 AND 500;
---------------------------------------------------------------
-- Query 14: Display orders from East and West Regions

SELECT *
FROM superstore
WHERE Region IN ('East', 'West');
---------------------------------------------------------------
-- Query 15: Display customers whose names start with 'A'

SELECT *
FROM superstore
WHERE `Customer Name` LIKE 'A%';
---------------------------------------------------------------
-- Query 16: Display orders with negative Profit

SELECT *
FROM superstore
WHERE Profit < 0;
---------------------------------------------------------------
-- Query 17: Display Office Supplies sold in the South Region

SELECT *
FROM superstore
WHERE Category = 'Office Supplies'
AND Region = 'South';

/*=============================================================
                SECTION 3
             ORDER BY & LIMIT
=============================================================*/

-- Query 18: Display Top 10 Highest Sales Orders

SELECT *
FROM superstore
ORDER BY Sales DESC
LIMIT 10;


---------------------------------------------------------------

-- Query 19: Display Top 10 Lowest Sales Orders

SELECT *
FROM superstore
ORDER BY Sales ASC
LIMIT 10;


---------------------------------------------------------------

-- Query 20: Display Top 10 Most Profitable Orders

SELECT *
FROM superstore
ORDER BY Profit DESC
LIMIT 10;


---------------------------------------------------------------

-- Query 21: Display Top 10 Least Profitable Orders

SELECT *
FROM superstore
ORDER BY Profit ASC
LIMIT 10;


---------------------------------------------------------------

-- Query 22: Display Top 10 Highest Discount Orders

SELECT *
FROM superstore
ORDER BY Discount DESC
LIMIT 10;


---------------------------------------------------------------

-- Query 23: Display Top 10 Highest Quantity Orders

SELECT *
FROM superstore
ORDER BY Quantity DESC
LIMIT 10;


---------------------------------------------------------------

-- Query 24: Display Top 10 Products by Sales

SELECT `Product Name`, Sales
FROM superstore
ORDER BY Sales DESC
LIMIT 10;


---------------------------------------------------------------

-- Query 25: Display Top 10 Customers by Profit

SELECT `Customer Name`, Profit
FROM superstore
ORDER BY Profit DESC
LIMIT 10;

/*=============================================================
                SECTION 4
           AGGREGATE FUNCTIONS
=============================================================*/

-- Query 26: Calculate Total Sales

SELECT SUM(Sales) AS Total_Sales
FROM superstore;


---------------------------------------------------------------

-- Query 27: Calculate Total Profit

SELECT SUM(Profit) AS Total_Profit
FROM superstore;


---------------------------------------------------------------

-- Query 28: Calculate Total Quantity Sold

SELECT SUM(Quantity) AS Total_Quantity
FROM superstore;


---------------------------------------------------------------

-- Query 29: Count Total Orders

SELECT COUNT(*) AS Total_Orders
FROM superstore;


---------------------------------------------------------------

-- Query 30: Count Unique Customers

SELECT COUNT(DISTINCT `Customer ID`) AS Total_Customers
FROM superstore;


---------------------------------------------------------------

-- Query 31: Count Unique Products

SELECT COUNT(DISTINCT `Product ID`) AS Total_Products
FROM superstore;


---------------------------------------------------------------

-- Query 32: Calculate Average Sales

SELECT AVG(Sales) AS Average_Sales
FROM superstore;


---------------------------------------------------------------

-- Query 33: Calculate Average Profit

SELECT AVG(Profit) AS Average_Profit
FROM superstore;


---------------------------------------------------------------

-- Query 34: Find Highest Sales

SELECT MAX(Sales) AS Highest_Sale
FROM superstore;


---------------------------------------------------------------

-- Query 35: Find Lowest Sales

SELECT MIN(Sales) AS Lowest_Sale
FROM superstore;


---------------------------------------------------------------

-- Query 36: Find Highest Profit

SELECT MAX(Profit) AS Highest_Profit
FROM superstore;


---------------------------------------------------------------

-- Query 37: Find Lowest Profit

SELECT MIN(Profit) AS Lowest_Profit
FROM superstore;


/*=============================================================
                SECTION 5
                  GROUP BY
=============================================================*/

-- Query 38: Total Sales by Region

SELECT Region,
       SUM(Sales) AS Total_Sales
FROM superstore
GROUP BY Region;


---------------------------------------------------------------

-- Query 39: Total Sales by Category

SELECT Category,
       SUM(Sales) AS Total_Sales
FROM superstore
GROUP BY Category;


---------------------------------------------------------------

-- Query 40: Total Sales by Sub-Category

SELECT `Sub-Category`,
       SUM(Sales) AS Total_Sales
FROM superstore
GROUP BY `Sub-Category`
ORDER BY Total_Sales DESC;


---------------------------------------------------------------

-- Query 41: Total Profit by Region

SELECT Region,
       SUM(Profit) AS Total_Profit
FROM superstore
GROUP BY Region;


---------------------------------------------------------------

-- Query 42: Average Sales by Category

SELECT Category,
       AVG(Sales) AS Average_Sales
FROM superstore
GROUP BY Category;


---------------------------------------------------------------

-- Query 43: Average Profit by Category

SELECT Category,
       AVG(Profit) AS Average_Profit
FROM superstore
GROUP BY Category;


---------------------------------------------------------------

-- Query 44: Total Quantity Sold by Category

SELECT Category,
       SUM(Quantity) AS Total_Quantity
FROM superstore
GROUP BY Category;


---------------------------------------------------------------

-- Query 45: Number of Orders by Ship Mode

SELECT `Ship Mode`,
       COUNT(*) AS Total_Orders
FROM superstore
GROUP BY `Ship Mode`
ORDER BY Total_Orders DESC;


---------------------------------------------------------------

-- Query 46: Number of Orders by Segment

SELECT Segment,
       COUNT(*) AS Total_Orders
FROM superstore
GROUP BY Segment;


---------------------------------------------------------------

-- Query 47: Total Sales by State

SELECT State,
       SUM(Sales) AS Total_Sales
FROM superstore
GROUP BY State
ORDER BY Total_Sales DESC;


---------------------------------------------------------------

-- Query 48: Total Profit by State

SELECT State,
       SUM(Profit) AS Total_Profit
FROM superstore
GROUP BY State
ORDER BY Total_Profit DESC;


---------------------------------------------------------------

-- Query 49: Average Discount by Category

SELECT Category,
       AVG(Discount) AS Average_Discount
FROM superstore
GROUP BY Category;

/*=============================================================
                SECTION 6
              BUSINESS QUERIES
=============================================================*/

-- Query 50: Display Top 10 Customers by Total Sales

SELECT `Customer Name`,
       SUM(Sales) AS Total_Sales
FROM superstore
GROUP BY `Customer Name`
ORDER BY Total_Sales DESC
LIMIT 10;


---------------------------------------------------------------

-- Query 51: Display Top 10 Products by Total Sales

SELECT `Product Name`,
       SUM(Sales) AS Total_Sales
FROM superstore
GROUP BY `Product Name`
ORDER BY Total_Sales DESC
LIMIT 10;


---------------------------------------------------------------

-- Query 52: Display Top 10 Most Profitable Products

SELECT `Product Name`,
       SUM(Profit) AS Total_Profit
FROM superstore
GROUP BY `Product Name`
ORDER BY Total_Profit DESC
LIMIT 10;


---------------------------------------------------------------

-- Query 53: Display Monthly Sales Trend

SELECT MONTHNAME(STR_TO_DATE(`Order Date`, '%d-%m-%Y')) AS Month,
       SUM(Sales) AS Total_Sales
FROM superstore
GROUP BY MONTH(STR_TO_DATE(`Order Date`, '%d-%m-%Y')),
         MONTHNAME(STR_TO_DATE(`Order Date`, '%d-%m-%Y'))
ORDER BY MONTH(STR_TO_DATE(`Order Date`, '%d-%m-%Y'));


---------------------------------------------------------------

-- Query 54: Display Total Sales by Customer Segment

SELECT Segment,
       SUM(Sales) AS Total_Sales
FROM superstore
GROUP BY Segment
ORDER BY Total_Sales DESC;


---------------------------------------------------------------

-- Query 55: Display Most Profitable Category

SELECT Category,
       SUM(Profit) AS Total_Profit
FROM superstore
GROUP BY Category
ORDER BY Total_Profit DESC;


---------------------------------------------------------------

-- Query 56: Display Top 10 States by Profit

SELECT State,
       SUM(Profit) AS Total_Profit
FROM superstore
GROUP BY State
ORDER BY Total_Profit DESC
LIMIT 10;


---------------------------------------------------------------

-- Query 57: Display Top 10 Cities by Sales

SELECT City,
       SUM(Sales) AS Total_Sales
FROM superstore
GROUP BY City
ORDER BY Total_Sales DESC
LIMIT 10;


---------------------------------------------------------------

-- Query 58: Display Products with Negative Total Profit

SELECT `Product Name`,
       SUM(Profit) AS Total_Profit
FROM superstore
GROUP BY `Product Name`
HAVING Total_Profit < 0
ORDER BY Total_Profit;


---------------------------------------------------------------

-- Query 59: Display Category-wise Average Discount

SELECT Category,
       AVG(Discount) AS Average_Discount
FROM superstore
GROUP BY Category
ORDER BY Average_Discount DESC;

/*=============================================================
                SECTION 7
              DATA VALIDATION
=============================================================*/

-- Query 60: Count Total Records

SELECT COUNT(*) AS Total_Records
FROM superstore;


---------------------------------------------------------------

-- Query 61: Check for NULL Values in Important Columns

SELECT *
FROM superstore
WHERE `Order ID` IS NULL
   OR `Customer ID` IS NULL
   OR Sales IS NULL
   OR Profit IS NULL;


---------------------------------------------------------------

-- Query 62: Check for Duplicate Order IDs

SELECT `Order ID`,
       COUNT(*) AS Duplicate_Count
FROM superstore
GROUP BY `Order ID`
HAVING COUNT(*) > 1;


---------------------------------------------------------------

-- Query 63: Count Distinct Customers

SELECT COUNT(DISTINCT `Customer ID`) AS Unique_Customers
FROM superstore;


---------------------------------------------------------------

-- Query 64: Count Distinct Products

SELECT COUNT(DISTINCT `Product ID`) AS Unique_Products
FROM superstore;


/*=============================================================
                END OF SQL ASSIGNMENT
=============================================================*/

-- All SQL queries have been executed successfully.
-- The Superstore dataset has been analyzed using:
-- ✓ WHERE Clause
-- ✓ ORDER BY & LIMIT
-- ✓ Aggregate Functions
-- ✓ GROUP BY
-- ✓ Business Queries
-- ✓ Data Validation

-- End of Week 2 Assignment


---------------------------------------------------------------

-- Query 65: Find Orders with Zero Profit

SELECT *
FROM superstore
WHERE Profit = 0;


---------------------------------------------------------------

-- Query 66: Find Orders with Negative Sales

SELECT *
FROM superstore
WHERE Sales < 0;

