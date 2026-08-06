# README.md

```markdown
# Uber Eats Data Analysis using Streamlit, Pandas, and SQLite

## Project Overview

This project is an interactive data analysis dashboard developed using **Python**, **Streamlit**, **Pandas**, and **SQLite**. It allows users to analyze Uber Eats restaurant and order datasets using predefined SQL queries through a user-friendly web interface.

The application supports two datasets:

- **Uber Eats Restaurant Dataset (CSV)**
- **Uber Eats Order Dataset (JSON)**

Users can select a dataset, choose an analysis question, and instantly view the corresponding SQL query results.

---

## Features

### Restaurant Dataset Analysis

The application provides insights such as:

- Top-rated restaurant locations
- Restaurant density across Bangalore
- Impact of online ordering on ratings
- Relationship between table booking and ratings
- Customer satisfaction by price segment
- Performance of budget, mid-range, and premium restaurants
- Most popular cuisines
- Highest-rated cuisines
- Underrated cuisines with fewer restaurants
- Premium restaurant opportunities by location
- High-demand but low-rated locations
- Effect of online ordering and table booking together
- Success factors based on multiple attributes
- Top-performing restaurants within each price segment

---

### Order Dataset Analysis

The dashboard also analyzes order information, including:

- Highest revenue-generating restaurants
- Dates with the highest number of orders
- Orders using discounts
- Revenue by payment method
- Daily revenue trends
- Most frequently used payment methods
- Percentage of discounted orders
- Total revenue generated
- Restaurants with the highest order volumes

---

## Technologies Used

- Python 3.x
- Streamlit
- Pandas
- NumPy
- SQLite3
- Regular Expressions (re)

---

## Project Structure

```

UberEats_Analysis/
│
├── app.py
├── README.md
├── requirements.txt
└── ubereats.db (created automatically)

````

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/UberEats-Analysis.git
cd UberEats-Analysis
````

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

Windows

```bash
.venv\Scripts\activate
```

Mac/Linux

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Run the Application

```bash
streamlit run app.py
```

The application opens automatically in your default web browser.

---

## How the Application Works

1. Select an analysis type from the sidebar.
2. The application downloads the selected dataset from Google Drive.
3. The dataset is cleaned and preprocessed using Pandas.
4. A SQLite database is created automatically.
5. Indexes are created for frequently queried columns.
6. The selected SQL query is executed.
7. Results are displayed in an interactive Streamlit table.

---

## Data Preprocessing

The application performs the following preprocessing steps:

* Removes duplicate records
* Removes missing ratings
* Converts ratings into numeric values
* Cleans restaurant cost values
* Handles missing cost values using the median
* Creates Price Segment categories
* Creates Rating Category labels

---

## SQLite Optimization

To improve query performance, SQLite indexes are automatically created for commonly queried columns:

* location
* cuisines
* price_segment
* online_order
* book_table
* rate

The database is rebuilt only when the selected dataset changes, reducing unnecessary processing.

---

## Performance Optimizations

The application includes several performance improvements:

* Streamlit data caching using `@st.cache_data`
* Resource caching using `@st.cache_resource`
* Session state management to avoid rebuilding the database
* Vectorized Pandas operations
* Efficient SQL queries
* SQLite indexing
* Automatic database connection management using context managers

---

## Error Handling

The application gracefully handles:

* Invalid Google Drive URLs
* Unsupported file formats
* Data loading errors
* SQL execution errors
* Empty datasets

---

## Future Enhancements

Possible future improvements include:

* Interactive charts using Plotly
* Dynamic SQL query generation
* Search and filter functionality
* Data export to CSV or Excel
* User-uploaded datasets
* Dashboard visualizations

---

## Author

**Priya**

Mini Project – Uber Eats Data Analysis using Streamlit, Pandas, and SQLite

---

## License

This project is developed for educational purposes.

```

### Review

This README matches your current codebase:
- ✅ Describes both restaurant and order dataset analyses.
- ✅ Documents the preprocessing steps implemented in `preprocess()`.
- ✅ Mentions the SQLite database creation and automatic index creation.
- ✅ Explains the caching strategy (`@st.cache_data`, `@st.cache_resource`, and `st.session_state`).
- ✅ Covers error handling and application workflow.

It is suitable for submission alongside your project.
```
