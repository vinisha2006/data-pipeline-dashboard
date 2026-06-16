from pathlib import Path
import sys

import pandas as pd
import plotly.express as px
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parent
SRC_PATH = PROJECT_ROOT / "src"
sys.path.append(str(SRC_PATH))

from load import read_sales_data  # noqa: E402
from pipeline import DATABASE_PATH, run_pipeline  # noqa: E402


st.set_page_config(page_title="Sales Data Pipeline Dashboard", layout="wide")


@st.cache_data
def load_dashboard_data(database_path: str) -> pd.DataFrame:
    data = read_sales_data(Path(database_path))
    data["order_date"] = pd.to_datetime(data["order_date"])
    return data


st.title("Sales Data Pipeline Dashboard")
st.caption("Python ETL project using Pandas, SQLite, Streamlit, and Plotly")

with st.sidebar:
    st.header("Pipeline")
    if st.button("Run ETL Pipeline", use_container_width=True):
        run_pipeline()
        st.cache_data.clear()
        st.success("Pipeline refreshed successfully.")

    st.header("Filters")

try:
    sales_data = load_dashboard_data(str(DATABASE_PATH))
except FileNotFoundError:
    st.warning("Database not found. Click the button below to run the ETL pipeline first.")
    if st.button("Create Database Now"):
        run_pipeline()
        st.cache_data.clear()
        st.rerun()
    st.stop()

with st.sidebar:
    min_date = sales_data["order_date"].min().date()
    max_date = sales_data["order_date"].max().date()
    date_range = st.date_input("Order date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)

    selected_regions = st.multiselect(
        "Region",
        options=sorted(sales_data["region"].unique()),
        default=sorted(sales_data["region"].unique()),
    )

    selected_categories = st.multiselect(
        "Category",
        options=sorted(sales_data["category"].unique()),
        default=sorted(sales_data["category"].unique()),
    )

if len(date_range) == 2:
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
else:
    start_date, end_date = sales_data["order_date"].min(), sales_data["order_date"].max()

filtered_data = sales_data[
    (sales_data["order_date"] >= start_date)
    & (sales_data["order_date"] <= end_date)
    & (sales_data["region"].isin(selected_regions))
    & (sales_data["category"].isin(selected_categories))
]

total_revenue = filtered_data["revenue"].sum()
total_profit = filtered_data["profit"].sum()
total_orders = filtered_data["order_id"].nunique()
average_order_value = total_revenue / total_orders if total_orders else 0

metric_1, metric_2, metric_3, metric_4 = st.columns(4)
metric_1.metric("Total Revenue", f"INR {total_revenue:,.0f}")
metric_2.metric("Total Profit", f"INR {total_profit:,.0f}")
metric_3.metric("Orders", f"{total_orders:,}")
metric_4.metric("Average Order Value", f"INR {average_order_value:,.0f}")

if filtered_data.empty:
    st.info("No data is available for the selected filters.")
    st.stop()

monthly_sales = filtered_data.groupby("month", as_index=False).agg({"revenue": "sum", "profit": "sum"})
category_sales = filtered_data.groupby("category", as_index=False)["revenue"].sum()
region_profit = filtered_data.groupby("region", as_index=False)["profit"].sum()
top_products = (
    filtered_data.groupby("product", as_index=False)
    .agg({"revenue": "sum", "quantity": "sum"})
    .sort_values("revenue", ascending=False)
    .head(10)
)

chart_1, chart_2 = st.columns(2)

with chart_1:
    st.subheader("Monthly Revenue and Profit")
    fig = px.line(monthly_sales, x="month", y=["revenue", "profit"], markers=True)
    fig.update_layout(xaxis_title="Month", yaxis_title="Amount")
    st.plotly_chart(fig, use_container_width=True)

with chart_2:
    st.subheader("Revenue by Category")
    fig = px.bar(category_sales, x="category", y="revenue", text_auto=".2s")
    fig.update_layout(xaxis_title="Category", yaxis_title="Revenue")
    st.plotly_chart(fig, use_container_width=True)

chart_3, chart_4 = st.columns(2)

with chart_3:
    st.subheader("Profit by Region")
    fig = px.bar(region_profit, x="region", y="profit", color="region", text_auto=".2s")
    fig.update_layout(xaxis_title="Region", yaxis_title="Profit", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with chart_4:
    st.subheader("Top Products by Revenue")
    fig = px.bar(top_products, x="revenue", y="product", orientation="h", text_auto=".2s")
    fig.update_layout(xaxis_title="Revenue", yaxis_title="Product", yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Cleaned Sales Data")
st.dataframe(filtered_data, use_container_width=True, hide_index=True)

csv_data = filtered_data.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download Filtered Data",
    data=csv_data,
    file_name="filtered_sales_data.csv",
    mime="text/csv",
)
