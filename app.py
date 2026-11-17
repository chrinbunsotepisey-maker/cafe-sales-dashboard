from pathlib import Path
import sqlite3

import streamlit as st

# Find the database and SQL files next to app.py.
project_folder = Path(__file__).resolve().parent
database_file = project_folder / "data" / "cafe_sales.db"
monthly_query_file = project_folder / "monthly_revenue.sql"
product_query_file = project_folder / "product_sales.sql"

# Read and run the two SQL queries.
monthly_query = monthly_query_file.read_text(encoding="utf-8-sig")
product_query = product_query_file.read_text(encoding="utf-8-sig")

database_address = database_file.as_uri() + "?mode=ro"
connection = sqlite3.connect(database_address, uri=True)

monthly_results = connection.execute(monthly_query).fetchall()
product_results = connection.execute(product_query).fetchall()

connection.close()

# Step 1: Show monthly revenue.
st.title("Café Sales Dashboard")
st.caption("Fictional café sales data")

for month, revenue_cents in monthly_results:
    revenue_dollars = revenue_cents / 100
    label = f"Revenue for {month}"
    display_value = f"${revenue_dollars:.2f}"

    st.metric(label, display_value)

# Step 2: Show the product sales table.
product_rows = []

for product_name, units_sold, revenue_cents in product_results:
    revenue_dollars = revenue_cents / 100
    row = {
        "Product": product_name,
        "Units sold": units_sold,
        "Revenue": f"${revenue_dollars:.2f}",
    }
    product_rows.append(row)

st.subheader("Product sales")
st.table(product_rows)

# Step 3: Show the revenue bar chart.
chart_rows = []

for product_name, _units_sold, revenue_cents in product_results:
    revenue_dollars = revenue_cents / 100
    chart_rows.append({
        "Product": product_name,
        "Revenue (USD)": revenue_dollars,
    })

st.subheader("Revenue by product")
st.bar_chart(chart_rows, x="Product", y="Revenue (USD)")