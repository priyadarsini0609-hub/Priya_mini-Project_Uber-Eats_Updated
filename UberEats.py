
# from os import path
# from unittest import result
# from urllib import response

import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
#import requests
#import mimetypes
#import os
import re

# Initialize the data_url variable
data_url = ""

# Initialize query variable
query = ""
file_id=""
file_name=""
path=""



# Defining the required functions

def get_file_id_from_url(data_url):

    # Extracts the file ID from a Google Drive URL.
    # Supports both 'drive.google.com/file/d/FILE_ID' and 'drive.google.com/uc?id=FILE_ID' formats.
   
    match = re.search(r'(?:id=)([a-zA-Z0-9_-]+)', data_url) # For uc?id=FILE_ID
    if match:
        return match.group(1)
    match = re.search(r'file/d/([a-zA-Z0-9_-]+)', data_url) # For file/d/FILE_ID
    if match:
        return match.group(1)
    return None

def get_file_extension(data_url):
    file_id=get_file_id_from_url(data_url)
    download_url = f'https://drive.google.com/uc?export=download&id={file_id}'
    # response = requests.get(download_url)
    # file_name=(response.headers.get("Content-Disposition"))
    #st.write(file_name)
    return download_url

@st.cache_data
def preprocess(df,file_name):

    # 1. Duplicate Removal  
    df=df.drop_duplicates().copy()

    #st.write(f"DataFrame shape after dropping rows with missing 'rate': {df.shape}")

    # 3. Rating Normalization
    if "rate" in df.columns:
        # 2. Missing Value Handling (dropping rows with missing 'rate')
        df=df.dropna(subset=['rate'])    
        #st.write(f"DataFrame shape before rating normalization: {df.shape}")
        df["rate"] = pd.to_numeric(
        df["rate"].astype(str).str.replace("/5", "", regex=False),
            errors="coerce"
        )
        rating_bins = [0, 2.5, 3.5, 4.0, 5.1]
        rating_labels = ['Low', 'Average', 'Good', 'Excellent']  
        df['rating_category'] = pd.cut(df['rate'], bins=rating_bins, labels=rating_labels, right=False)
    
        # 4. Cost Standardization
        if "approx_cost(for two people)" in df.columns:
            cost = "approx_cost(for two people)"

            df[cost] = pd.to_numeric(
                df[cost].astype(str).str.replace(",", "", regex=False),
                errors="coerce"
            )

            median_cost = df[cost].median()
            df[cost] = df[cost].fillna(median_cost)

            df["price_segment"] = pd.cut(
                df[cost],
                bins=[0, 500, 1000, 2000, np.inf],
                labels=["Budget", "Mid-range", "Expensive", "Very Expensive"],
                right=False
            )
    return df

def load_and_process_data(data_url,file_name):
    try:
        download_url = get_file_extension(data_url)
        if ".csv" in file_name:
            df = pd.read_csv(download_url)
            #st.write(f"DataFrame shape after loading CSV: {df.shape}")
        elif ".json" in file_name:
            df = pd.read_json(download_url)
            #st.write(f"DataFrame shape after loading JSON: {df.shape}")
        else:
            st.error("Unsupported file")
            return pd.DataFrame()
        
        return preprocess(df,file_name)
    except Exception as e:
            st.error(f"Error loading or processing data: {e}")
            return pd.DataFrame() # Return empty DataFrame on error  
def select_query(Questions, Queries):
    #st.write(f"Selected Question: {Questions} and Query: {query}" )
    query = Queries.get(f"Questions[{Questions.split('.')[0]}]", "")
    #st.write(f"Selected Question: {Questions} and Query: {query}" )
    return query

#Creating a SQLite database and storing the cleaned data in it

@st.cache_resource
def create_database(df):
    conn = sqlite3.connect("ubereats.db")

    try:
        df.to_sql("cleaned_data", conn, if_exists="replace", index=False)

        
        #creating indexes for faster query execution        
        cursor = conn.cursor()
        if('location' in df.columns):
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_location ON cleaned_data(location)")
        if('price_segment' in df.columns):
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_price ON cleaned_data(price_segment)")
        if('cuisines' in df.columns):
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_cuisine ON cleaned_data(cuisines)")
        if('online_order' in df.columns):
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_online ON cleaned_data(online_order)")
        if('book_table' in df.columns):
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_book ON cleaned_data(book_table)")
        if('rate' in df.columns):
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_rate ON cleaned_data(rate)")
        conn.commit()
    finally:
        conn.close()

def execute_query(query):
    conn = sqlite3.connect("ubereats.db")

    try:
        df = pd.read_sql(query, conn)
        return df

    except Exception as e:
        st.error(f"Error executing query: {e}")
        return pd.DataFrame() # Return empty DataFrame on error
       
    finally:
        conn.close()

st.set_page_config(layout="wide")
# Add a selection widget in the sidebar
analysis_Options = ["Please select an analysis", "UberEats_Dataset Analysis", "UberEats_Order Analysis"]
analysis_choice = st.sidebar.selectbox(
    "Analysis", analysis_Options
)

if analysis_choice == analysis_Options[0]:
    st.title('Welcome to Uber Eats Order Data Analysis:' + '\n' + ' Please select an analysis from the dropdown in the sidebar.')
else:
    if analysis_choice == analysis_Options[1]:
        st.title(analysis_choice)
        file_name = 'UberEats_Dataset.csv'
        # Google Drive URL for direct download
        data_url = 'https://drive.google.com/uc?export=download&id=19QzAIMQi3i4ggwWHXx325Y7aVIH3dyUx'

        #Defining Restaurant_Data Questions
        Data_Questions=["Select a Question",     
        "1.    Which Bangalore locations have the highest average restaurant ratings?",
        "2.    Which locations are over-saturated with restaurants?", 
        "3.    Does online ordering improve restaurant ratings?", 
        "4.    Does table booking correlate with higher customer ratings?",
        "5.    What price range delivers the best customer satisfaction?",
        "6.    How do low, mid, and premium-priced restaurants perform in terms of ratings?",   
        "7.    Which cuisines are most common in Bangalore?",
        "8.    Which cuisines receive the highest average ratings?",
        "9.    Which cuisines perform well despite having fewer restaurants?",
        "10.   Which locations are ideal for premium restaurant onboarding?", 
        "11.   Which locations show high demand but lower average ratings?",
        "12.   Do restaurants offering both online ordering and table booking perform better?",
        "13.   What combination of factors maximizes restaurant success on Uber Eats?",
        "14.   Which restaurants are top performers within each pricing segment?"
        ]

        # Defining Restaurant_Data Queries
        Data_queries = {
            "Questions[1]": """
            SELECT
                location,
                AVG(rate) AS average_rating
            FROM
                cleaned_data
            GROUP BY
                location
            ORDER BY            
                average_rating DESC
            LIMIT 10;
            """,

        "Questions[2]": """
            SELECT
                location,
                COUNT(*) AS restaurant_count
            FROM
                cleaned_data
            GROUP BY
                location
            ORDER BY
                restaurant_count DESC
            LIMIT 10;
            """,

        "Questions[3]":  """
            SELECT
                online_order,
                AVG(rate) AS average_rating,
                COUNT(*) AS restaurant_count
            FROM
                cleaned_data
            GROUP BY
                online_order
            ORDER BY
                average_rating DESC;
            """,

        "Questions[4]":"""
            SELECT
                book_table,
                AVG(rate) AS average_rating,
                COUNT(*) AS restaurant_count
            FROM
                cleaned_data
            GROUP BY
                book_table
            ORDER BY
                average_rating DESC;
            """,

        "Questions[5]": """
            SELECT
                price_segment,
                AVG(rate) AS average_rating,
                COUNT(*) AS restaurant_count
            FROM
                cleaned_data
            GROUP BY
                price_segment
            ORDER BY
                average_rating DESC;
            """,

        "Questions[6]":  """
            SELECT
                price_segment,
                AVG(rate) AS average_rating,
                COUNT(*) AS restaurant_count
            FROM
                cleaned_data
            GROUP BY
                price_segment
            ORDER BY
                average_rating DESC;
            """,

        "Questions[7]": """
            SELECT
                cuisines,
                COUNT(*) AS restaurant_count
            FROM
                cleaned_data
            GROUP BY
                cuisines
            ORDER BY
                restaurant_count DESC
            LIMIT 10;
            """,

        "Questions[8]": """
            SELECT
                cuisines,
                AVG(rate) AS average_rating,
                COUNT(*) AS restaurant_count
            FROM
                cleaned_data
            GROUP BY
                cuisines
            ORDER BY
                average_rating DESC
            LIMIT 10;
            """,

        "Questions[9]":  """
            SELECT
                cuisines,
                AVG(rate) AS average_rating,
                COUNT(*) AS restaurant_count
            FROM
                cleaned_data
            GROUP BY
                cuisines
            HAVING
                restaurant_count < 10
            ORDER BY
                average_rating DESC;
            """,
        
        "Questions[10]":   """
            SELECT
                location,
                AVG(rate) AS average_rating,
                COUNT(*) AS restaurant_count
            FROM
                cleaned_data
            WHERE
                price_segment IN ('Expensive', 'Very Expensive')
            GROUP BY
                location
            ORDER BY
                average_rating DESC;
            """,

        "Questions[11]":   """
            SELECT
                location,
                AVG(rate) AS average_rating,
                COUNT(*) AS restaurant_count
            FROM
                cleaned_data
            GROUP BY
                location
            HAVING
                restaurant_count > 20 AND average_rating < 3.5
            ORDER BY
                restaurant_count DESC;
            """,
        "Questions[12]":   """
            SELECT
                online_order,
                book_table,
                AVG(rate) AS average_rating,
                COUNT(*) AS restaurant_count
            FROM
                cleaned_data
            GROUP BY
                online_order, book_table
            ORDER BY
                average_rating DESC;
            """,
        "Questions[13]":    """
            SELECT
                online_order,
                book_table,
                price_segment,
                AVG(rate) AS average_rating,
                COUNT(*) AS restaurant_count
            FROM
                cleaned_data
            GROUP BY
                online_order, book_table, price_segment
            ORDER BY
                average_rating DESC;
            """,

        "Questions[14]":  """
            SELECT
                name,
                price_segment,
                AVG(rate) AS average_rating,
                COUNT(*) AS restaurant_count
            FROM
                cleaned_data
            GROUP BY
                name, price_segment;
            """        
        }
        Ques = st.selectbox("Choose a question", Data_Questions)
        if not Ques is Data_Questions[0]:
            query=select_query(Ques, Data_queries)
        else:
            st.write("Please select an analysis from the dropdown to see the analysis results.")

    elif analysis_choice ==analysis_Options[2]:
        st.title(analysis_choice)
        file_name = 'UberEats_Order_Dataset.json'
        data_url = 'https://drive.google.com/file/d/14bII0uj7A8OyBqruIy8n_CPpGyPoYOoA/view?usp=sharing'

        #Defining Restaurant_Order Questions
        Order_Questions = ["Select a Question",
        "1. Which restaurant generated the highest revenue?",
        "2. Which day had the highest number of orders?",
        "3. How many orders used discounts?",
        "4. Which payment method generated the highest revenue?",
        "5. What is the daily revenue trend?",
        "6. Which dates had the highest number of orders?",
        "7. Which payment method was used most frequently?",
        "8. What percentage of orders used discounts?",
        "9. What is the total revenue generated?",
        "10. Which restaurants received the highest number of orders?"
        ]

         # Defining Order_Queries
        
        # Defining Order_Data Queries
        
        Order_queries = {
        "Questions[1]": """
            SELECT
            restaurant_name,
            SUM(order_value) AS total_revenue
            FROM
                cleaned_data
            GROUP BY
                restaurant_name
            ORDER BY            
                total_revenue DESC
            LIMIT 10;
            """,
        
        "Questions[2]": """
        SELECT
            order_date,
            COUNT(*) AS order_count
        FROM
            cleaned_data
        GROUP BY
            order_date
        ORDER BY
            order_count DESC
        LIMIT 10;
        """,
    
        "Questions[3]": """
            SELECT
            COUNT(*) AS discount_order_count
        FROM
            cleaned_data
        WHERE
            discount_used = 'Yes';
            """,
    
        "Questions[4]":"""
        SELECT
            payment_method,
            SUM(order_value) AS total_revenue
        FROM
            cleaned_data
        GROUP BY
            payment_method
        ORDER BY
            total_revenue DESC;
        """,

        "Questions[5]":  """ 
        SELECT order_date, SUM(order_value) AS daily_revenue 
        FROM cleaned_data 
        GROUP BY order_date 
        ORDER BY order_date
        LIMIT 10; 
        """,
        
        "Questions[6]": """ 
        SELECT order_date, COUNT(*) AS total_orders 
        FROM cleaned_data 
        GROUP BY order_date 
        ORDER BY total_orders 
        DESC LIMIT 10;
        """,
        
        "Questions[7]": """ 
        SELECT payment_method, COUNT(*) AS total_orders 
        FROM cleaned_data 
        GROUP BY payment_method 
        ORDER BY total_orders DESC; 
        """,
        
        "Questions[8]": """ 
        SELECT ROUND(100.0 * SUM(CASE WHEN discount_used='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) 
        AS discount_percentage FROM cleaned_data;
        """,
        
        "Questions[9]":   """ 
        SELECT SUM(order_value) AS total_revenue FROM cleaned_data
        """,

        "Questions[10]": """ 
        SELECT restaurant_name, COUNT(*) AS total_orders 
        FROM cleaned_data 
        GROUP BY restaurant_name ORDER BY total_orders 
        DESC LIMIT 10;
        """ 
        } 
        Ques = st.selectbox("Choose a question", Order_Questions)
        if not Ques is Order_Questions[0]:
            query=select_query(Ques, Order_queries)
            #st.write(f"Executing Query for: {Ques}")
        else:
            st.write("Please select an analysis from the dropdown to see the analysis results.")
    else:
        st.write("Please select an analysis from the dropdown to see the analysis results.")

if not data_url =="": 
    processed_df = load_and_process_data(data_url,file_name)
    create_database(processed_df) 

    if not processed_df.empty and processed_df is not None:
        if not query == "" and not query is None:       
            #st.write(f"Executing Query for: {Ques}")
            
            query_result = execute_query(query)   
            #st.write(f"Query: {query}")
            st.write(f"Query Result for: {Ques}") 

            # Display the query result in a user-friendly format from index 1 instead of 0
            
            df_display = query_result.reset_index(drop=True)
            df_display.index = df_display.index + 1
            st.dataframe(df_display)

        else:
            st.write("Query is empty. Please select a question to execute the query.")   

    else:   
        st.write("Dataframe Empty")
else:
    processed_df = pd.DataFrame()  # Create an empty DataFrame if no data URL is provided
    st.write("Please select an analysis from the dropdown to see the analysis results.")


   