import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(layout="wide")
st.title('Uber Eats Bangalore Data Analysis')

# Google Drive URL for direct download
data_url = 'https://drive.google.com/uc?export=download&id=19QzAIMQi3i4ggwWHXx325Y7aVIH3dyUx'

@st.cache_data
def load_and_process_data():
    try:
        df = pd.read_csv(data_url)
        st.success("Data loaded successfully!")

        # 1. Duplicate Removal
        initial_rows = df.shape[0]
        df.drop_duplicates(inplace=True)
        st.write(f"Number of duplicate rows removed: {initial_rows - df.shape[0]}")

        # 2. Missing Value Handling (dropping rows with missing 'rate')
        df.dropna(subset=['rate'], inplace=True)
        st.write(f"DataFrame shape after dropping rows with missing 'rate': {df.shape}")

        # 3. Rating Normalization
        df['rate'] = df['rate'].astype(str).str.replace('/5', '', regex=False)
        df['rate'] = pd.to_numeric(df['rate'], errors='coerce')
        df = df.dropna(subset=['rate']).copy() # Drop rows where rate became NaN after conversion

        # 4. Cost Standardization
        df['approx_cost(for two people)'] = df['approx_cost(for two people)'].astype(str).str.replace(',', '', regex=False)
        df['approx_cost(for two people)'] = pd.to_numeric(df['approx_cost(for two people)'], errors='coerce')
        df['approx_cost(for two people)'] = df['approx_cost(for two people)'].fillna(df['approx_cost(for two people)'].median())

        # 5. Feature Engineering - Pricing Segments
        bins = [0, 500, 1000, 2000, df['approx_cost(for two people)'].max() + 1]
        labels = ['Budget', 'Mid-range', 'Expensive', 'Very Expensive']
        df['price_segment'] = pd.cut(df['approx_cost(for two people)'], bins=bins, labels=labels, right=False)

        # 6. Feature Engineering - Rating Categories
        rating_bins = [0, 2.5, 3.5, 4.0, 5.1]
        rating_labels = ['Low', 'Average', 'Good', 'Excellent']
        df['rating_category'] = pd.cut(df['rate'], bins=rating_bins, labels=rating_labels, right=False)

        return df

    except Exception as e:
        st.error(f"Error loading or processing data: {e}")
        return pd.DataFrame() # Return empty DataFrame on error

processed_df = load_and_process_data()

if not processed_df.empty:
    st.header("Processed Data Preview")
    st.dataframe(processed_df.head())

    # Connect to an in-memory SQLite database
    conn = sqlite3.connect(':memory:')

    # Save the cleaned DataFrame to a SQL table
    processed_df.to_sql('cleaned_data', conn, if_exists='replace', index=False)
    st.success("Cleaned data loaded into in-memory SQLite database.")

    st.header("Analysis Results")


   




   #
Yesterday 4:51 PM

UberEats(1).py
Python

The uploaded file shows why you're getting the error. The relevant section is: 


Your code is essentially:

file_path = "D:\\Priya_mini Project_Uber Eats\\Streamlit application\\Uber_Eats_data.csv"

try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    print("File not found")
except Exception as e:
    print(f"Error loading data: {e}")

initial_rows = df.shape[0]
Why NameError happens
If pd.read_csv() fails (for example, because the file path is wrong or the CSV has an error), the except block prints an error, but df is never created.

Then Python reaches:

initial_rows = df.shape[0]
and raises:

NameError: name 'df' is not defined
Fix 1 (recommended)
Stop execution if the file cannot be loaded:

import streamlit as st
import pandas as pd

file_path = r"D:\Priya_mini Project_Uber Eats\Streamlit application\Uber_Eats_data.csv"

try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    st.error(f"File not found: {file_path}")
    st.stop()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

initial_rows = df.shape[0]
Fix 2: Check your file path
Your code uses:

"D:\Priya_mini Project_Uber Eats\Streamlit application\Uber_Eats_data.csv"
Verify that:

Uber_Eats_data.csv actually exists there.

The filename matches exactly (including capitalization and underscores).

You're not running the app from a different project folder.

A better approach is to keep the CSV in the same project folder as your Streamlit app and use:

df = pd.read_csv("Uber_Eats_data.csv")
I also noticed another issue
You're using print() in a Streamlit app. 


Instead of:

print(df.head())
use:

st.write(df.head())
or

st.dataframe(df.head())
so the output appears in the Streamlit interface.

To pinpoint the exact cause
Please tell me what error message appears before:

NameError: name 'df' is not defined
For example, is it:

FileNotFoundError

ParserError

UnicodeDecodeError

or something else?

That earlier message is what caused df not to be created.


Today 11:41 AM
3.Streamlit Application (No Visualization)
The Streamlit application is designed without graphical visualizations and is used exclusively for:
Executing SQL queries


Displaying DataFrame-based results


Allowing business users to explore insights through structured tabular outputs



Application Structure
1. Dashboard Page
Provides multiple filtering options for users


Allows users to filter and retrieve data dynamically from the SQL database


Displays the filtered results in DataFrame/table format


All filtering logic is implemented strictly using SQL queries


2. Q&A Page
Displays analysis for 10 predefined business questions


Each answer is generated through SQL-based computation


Results are presented in structured table format within Streamlit
      3. Order Data Integration & Custom Analytical Q&A
In addition to existing datasets:
The generated order dataset (originally stored in JSON format) will be imported and stored in the SQL database as a structured table.


All order-related analysis will also be executed using SQL queries.


A custom Q&A module will be implemented specifically for the order dataset
The system will support answering as many meaningful business queries as possible, leveraging SQL-based computation for consistency and efficiency

Based on your project requirements, your Streamlit application should not contain any charts or visualizations. It should only use SQL queries and display the results as DataFrames/tables. A suitable application structure is as follows:

Uber Eats Analytics - Streamlit Application
1. Dashboard Page
Purpose
Allow users to explore restaurant data using filters. Every filter selection should generate an SQL query, and the output should be displayed as a table.

Filters
City / Location

Restaurant Type

Online Order (Yes/No)

Table Booking (Yes/No)

Cuisine

Rating Range

Cost for Two

Votes Range

Workflow
User selects filters.

Streamlit generates the corresponding SQL query.

SQL retrieves matching records.

Display the result using:

st.dataframe(result_df)
No graphs or charts should be included.

Example SQL:

SELECT *
FROM restaurants
WHERE location = ?
AND online_order = ?
AND rest_type = ?;
2. Business Q&A Page
This page contains 10 predefined SQL-based business questions.

Example questions include:

Top 10 highest-rated restaurants.

Restaurants accepting online orders.

Restaurants with table booking.

Average rating by restaurant type.

Average cost by location.

Most popular cuisines.

Restaurants with the highest votes.

Number of restaurants in each location.

Restaurants with rating greater than 4.

Restaurants serving multiple cuisines.

Each button executes an SQL query such as:

SELECT name, rate
FROM restaurants
ORDER BY rate DESC
LIMIT 10;
Display the result using:

st.dataframe(result)
3. Order Data Integration
The generated order dataset (stored in JSON format) should first be imported into SQL.

Example workflow:

orders.json
      ↓
Pandas
      ↓
SQLite Table (orders)
      ↓
SQL Queries
      ↓
Streamlit DataFrame
Example import:

import json
import pandas as pd
import sqlite3

with open("orders.json") as f:
    orders = json.load(f)

df_orders = pd.DataFrame(orders)

conn = sqlite3.connect("ubereats.db")
df_orders.to_sql("orders", conn, if_exists="replace", index=False)
4. Custom Order Analytics Page
Create a separate page dedicated to the orders table. Every answer should be generated using SQL.

Example business questions:

Total number of orders.

SELECT COUNT(*) AS Total_Orders
FROM orders;
Total revenue.

SELECT SUM(order_amount) AS Revenue
FROM orders;
Average order value.

SELECT AVG(order_amount) AS Average_Order_Value
FROM orders;
Highest-value order.

SELECT *
FROM orders
ORDER BY order_amount DESC
LIMIT 1;
Most ordered restaurant.

SELECT restaurant_name,
COUNT(*) AS Orders
FROM orders
GROUP BY restaurant_name
ORDER BY Orders DESC;
Orders by payment method.

SELECT payment_method,
COUNT(*) AS Orders
FROM orders
GROUP BY payment_method;
Orders by delivery status.

SELECT delivery_status,
COUNT(*)
FROM orders
GROUP BY delivery_status;
Top customers.

SELECT customer_name,
COUNT(*) AS Orders
FROM orders
GROUP BY customer_name
ORDER BY Orders DESC;
Revenue by restaurant.

SELECT restaurant_name,
SUM(order_amount) AS Revenue
FROM orders
GROUP BY restaurant_name
ORDER BY Revenue DESC;
Average delivery time.

SELECT AVG(delivery_time)
FROM orders;
You can add additional SQL-based analyses such as:

Orders by date

Peak ordering hours

Cancelled orders

Delivered vs. pending orders

Orders by city

Revenue by city

Revenue by cuisine

Payment method distribution

Discount usage

Customer repeat orders

Suggested Streamlit Navigation
Uber Eats Analytics

├── Dashboard
│     ├── SQL Filters
│     └── DataFrame Results
│
├── Business Q&A
│     ├── 10 Predefined SQL Questions
│     └── DataFrame Results
│
├── Order Analytics
│     ├── Order Dataset SQL Queries
│     ├── Custom Business Questions
│     └── DataFrame Results
│
└── About
This structure fully aligns with your stated requirements: all data retrieval and analysis are performed using SQL queries, and all outputs are displayed as structured DataFrames/tables in Streamlit, with no graphical visualizations.


need code for tis 
├── Dashboard
│     ├── SQL Filters
│     └── DataFrame Results
│
├── Business Q&A
│     ├── 10 Predefined SQL Questions
│     └── DataFrame Results
│
├── Order Analytics
│     ├── Order Dataset SQL Queries
│     ├── Custom Business Questions
│     └── DataFrame Results
│
└── About

Below is a complete Streamlit application structure that matches your project requirements. It uses SQLite + SQL queries only and displays results using DataFrames (no charts).

Project Structure
UberEats/
│
├── UberEats.py
├── ubereats.db
├── orders.json
└── requirements.txt
UberEats.py
import streamlit as st
import pandas as pd
import sqlite3

# ---------------------------
# Database Connection
# ---------------------------

conn = sqlite3.connect("ubereats.db", check_same_thread=False)

# ---------------------------
# Sidebar
# ---------------------------

st.sidebar.title("Uber Eats Analytics")

page = st.sidebar.radio(
    "Select Page",
    [
        "Dashboard",
        "Business Q&A",
        "Order Analytics",
        "About"
    ]
)

# ===================================================
# DASHBOARD
# ===================================================

if page == "Dashboard":

    st.title("Dashboard")

    # -----------------------
    # Filters
    # -----------------------

    locations = pd.read_sql(
        "SELECT DISTINCT location FROM restaurants ORDER BY location",
        conn
    )["location"].tolist()

    restaurant_types = pd.read_sql(
        "SELECT DISTINCT rest_type FROM restaurants ORDER BY rest_type",
        conn
    )["rest_type"].tolist()

    online = ["Yes","No"]

    location = st.selectbox("Location", ["All"] + locations)

    rest_type = st.selectbox(
        "Restaurant Type",
        ["All"] + restaurant_types
    )

    online_order = st.selectbox(
        "Online Order",
        ["All"] + online
    )

    # -----------------------
    # SQL Query
    # -----------------------

    query = "SELECT * FROM restaurants WHERE 1=1"

    if location != "All":
        query += f" AND location='{location}'"

    if rest_type != "All":
        query += f" AND rest_type='{rest_type}'"

    if online_order != "All":
        query += f" AND online_order='{online_order}'"

    df = pd.read_sql(query, conn)

    st.write("### Filtered Results")

    st.dataframe(df)

# ===================================================
# BUSINESS Q&A
# ===================================================

elif page == "Business Q&A":

    st.title("Business Questions")

    questions = {

        "Top 10 Highest Rated Restaurants":
        """
        SELECT name, rate
        FROM restaurants
        ORDER BY rate DESC
        LIMIT 10
        """,

        "Top 10 Most Voted Restaurants":
        """
        SELECT name,votes
        FROM restaurants
        ORDER BY votes DESC
        LIMIT 10
        """,

        "Average Rating by Restaurant Type":
        """
        SELECT rest_type,
        AVG(rate) AS Average_Rating
        FROM restaurants
        GROUP BY rest_type
        """,

        "Restaurants Accepting Online Orders":
        """
        SELECT name,location
        FROM restaurants
        WHERE online_order='Yes'
        """,

        "Restaurants with Table Booking":
        """
        SELECT name,location
        FROM restaurants
        WHERE book_table='Yes'
        """,

        "Average Cost by Location":
        """
        SELECT location,
        AVG(approx_cost)
        FROM restaurants
        GROUP BY location
        """,

        "Restaurant Count by Location":
        """
        SELECT location,
        COUNT(*) AS Restaurants
        FROM restaurants
        GROUP BY location
        ORDER BY Restaurants DESC
        """,

        "Most Popular Cuisines":
        """
        SELECT cuisines,
        COUNT(*) AS Count
        FROM restaurants
        GROUP BY cuisines
        ORDER BY Count DESC
        LIMIT 10
        """,

        "Restaurants Rating Above 4":
        """
        SELECT name,rate
        FROM restaurants
        WHERE rate>4
        """,

        "Top Costly Restaurants":
        """
        SELECT name,
        approx_cost
        FROM restaurants
        ORDER BY approx_cost DESC
        LIMIT 10
        """
    }

    question = st.selectbox(
        "Choose Question",
        list(questions.keys())
    )

    if st.button("Execute SQL"):

        result = pd.read_sql(
            questions[question],
            conn
        )

        st.dataframe(result)

# ===================================================
# ORDER ANALYTICS
# ===================================================

elif page == "Order Analytics":

    st.title("Order Analytics")

    order_queries = {

        "Total Orders":
        """
        SELECT COUNT(*) AS Total_Orders
        FROM orders
        """,

        "Total Revenue":
        """
        SELECT SUM(order_amount)
        AS Revenue
        FROM orders
        """,

        "Average Order Value":
        """
        SELECT AVG(order_amount)
        AS Average_Order
        FROM orders
        """,

        "Highest Order":
        """
        SELECT *
        FROM orders
        ORDER BY order_amount DESC
        LIMIT 1
        """,

        "Revenue by Restaurant":
        """
        SELECT restaurant_name,
        SUM(order_amount) Revenue
        FROM orders
        GROUP BY restaurant_name
        ORDER BY Revenue DESC
        """,

        "Orders by Payment":
        """
        SELECT payment_method,
        COUNT(*) Orders
        FROM orders
        GROUP BY payment_method
        """,

        "Orders by Status":
        """
        SELECT delivery_status,
        COUNT(*) Total
        FROM orders
        GROUP BY delivery_status
        """,

        "Top Customers":
        """
        SELECT customer_name,
        COUNT(*) Orders
        FROM orders
        GROUP BY customer_name
        ORDER BY Orders DESC
        LIMIT 10
        """,

        "Orders by City":
        """
        SELECT city,
        COUNT(*) Orders
        FROM orders
        GROUP BY city
        """,

        "Average Delivery Time":
        """
        SELECT AVG(delivery_time)
        AS Avg_Delivery_Time
        FROM orders
        """
    }

    order_question = st.selectbox(
        "Select Analysis",
        list(order_queries.keys())
    )

    if st.button("Run Query"):

        result = pd.read_sql(
            order_queries[order_question],
            conn
        )

        st.dataframe(result)

# ===================================================
# ABOUT
# ===================================================

else:

    st.title("About")

    st.write("""
### Uber Eats Analytics

This application is developed using:

- Streamlit
- SQLite
- SQL Queries
- Pandas

### Features

✔ Dashboard Filters

✔ SQL-Based Business Q&A

✔ Order Analytics

✔ DataFrame Outputs Only

✔ No Graphical Visualizations

### Developed For

Mini Project - Uber Eats Data Analytics
""")
Database Tables Required
Your SQLite database (ubereats.db) should contain at least these tables:

restaurants
Columns such as:

name

location

rest_type

online_order

book_table

rate

votes

approx_cost

cuisines

orders
Columns such as:

order_id

customer_name

restaurant_name

city

order_amount

payment_method

delivery_status

delivery_time

This provides the four-page Streamlit application you described:

Dashboard with SQL-based filters and tabular results.

Business Q&A with 10 predefined SQL queries.

Order Analytics with SQL analyses on the orders table.

About page describing the project.#