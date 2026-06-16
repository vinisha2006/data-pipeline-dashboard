# Sales Data Pipeline Dashboard

This is a beginner-friendly Python project that demonstrates a complete data pipeline:

1. Extract raw sales data from a CSV file.
2. Transform and clean the data using Pandas.
3. Load the cleaned data into a SQLite database.
4. Display business insights in an interactive Streamlit dashboard.

## Why This Project Is Useful

This project is good for LinkedIn, GitHub, and interviews because it shows practical data engineering and analytics skills:

- Python programming
- Data cleaning with Pandas
- ETL pipeline design
- SQL database storage
- Dashboard creation
- Business metric analysis

## Tech Stack

- Python
- Pandas
- SQLite
- Streamlit
- Plotly

## Project Structure

```text
data-pipeline-dashboard/
├── data/
│   ├── raw_sales.csv
│   └── cleaned_sales.csv        # Created after running the pipeline
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── pipeline.py
├── dashboard.py
├── requirements.txt
├── sales_dashboard.db           # Created after running the pipeline
└── README.md
```

## Setup Instructions

Open a terminal in the project folder:

```bash
cd data-pipeline-dashboard
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run The ETL Pipeline

Run this command first:

```bash
python src/pipeline.py
```

This creates:

- `data/cleaned_sales.csv`
- `sales_dashboard.db`

## Run The Dashboard

Start the Streamlit dashboard:

```bash
streamlit run dashboard.py
```

Streamlit will show a local browser URL, usually:

```text
http://localhost:8501
```

## What The Dashboard Shows

The dashboard includes:

- Total revenue
- Total profit
- Number of orders
- Average order value
- Monthly revenue and profit trend
- Revenue by category
- Profit by region
- Top products by revenue
- Filtered data table
- Download button for filtered data

## How The Pipeline Works

### 1. Extract

`src/extract.py` reads raw sales data from:

```text
data/raw_sales.csv
```

### 2. Transform

`src/transform.py` cleans the data by:

- Removing duplicate orders
- Removing invalid rows
- Converting dates into proper date format
- Converting quantity and price columns into numbers
- Standardizing text columns
- Creating new columns:
  - `revenue`
  - `cost`
  - `profit`
  - `month`

### 3. Load

`src/load.py` stores the cleaned data in a SQLite database table called:

```text
sales
```

### 4. Dashboard

`dashboard.py` reads the SQLite database and creates interactive charts using Streamlit and Plotly.

## Ideas To Improve This Project

After learning the basic version, you can improve it by adding:

- API data extraction
- PostgreSQL instead of SQLite
- Scheduled pipeline runs
- User login
- Forecasting future sales
- Docker support
- Cloud deployment
- More realistic business data

## LinkedIn Post Example

```text
I built a Sales Data Pipeline Dashboard using Python.

The project extracts raw sales data from a CSV file, cleans it using Pandas, stores the cleaned data in SQLite, and displays business insights through an interactive Streamlit dashboard.

Key features:
- Automated ETL pipeline
- Revenue and profit analysis
- Region and category filters
- Top product insights
- Downloadable cleaned data

Tech stack:
Python, Pandas, SQLite, Streamlit, Plotly
```
