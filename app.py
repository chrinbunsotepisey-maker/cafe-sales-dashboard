import csv
import os
import sqlite3
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory

import streamlit as st


project_folder = Path(__file__).resolve().parent
database_file = project_folder / "data" / "cafe_sales.db"

st.title("Café Sales Dashboard")
st.caption("Fictional café sales data")

# Use the local database or create a temporary one for this demo session.
demo_mode = os.getenv("CAFE_DEMO") == "1" or not database_file.is_file()

if demo_mode:
    st.info("Demo mode. Your sales are saved for this session only.")

    if "demo_folder" not in st.session_state:
        demo_folder = TemporaryDirectory()
        demo_file = Path(demo_folder.name) / "cafe_demo.db"

        schema = (project_folder / "schema.sql").read_text(
            encoding="utf-8-sig"
        )
        sample_data = (project_folder / "sample_data.sql").read_text(
            encoding="utf-8-sig"
        )

        demo_connection = sqlite3.connect(demo_file)
        try:
            demo_connection.execute("PRAGMA foreign_keys = ON")
            demo_connection.executescript(schema)
            demo_connection.executescript(sample_data)
        finally:
            demo_connection.close()

        st.session_state["demo_folder"] = demo_folder

    database_file = Path(st.session_state["demo_folder"].name) / "cafe_demo.db"

if not database_file.is_file():
    st.error("The café database could not be found. Restart the app and try again.")
    st.stop()

connection = sqlite3.connect(database_file)
connection.execute("PRAGMA foreign_keys = ON")

record_tab, report_tab = st.tabs(["Record a Sale", "Sales Report"])

# Record a Sale
with record_tab:
    st.subheader("New sale")

    order_number = st.session_state.get("order_number", 0)
    last_receipt_id = st.session_state.get("last_receipt_id")

    if last_receipt_id is not None:
        st.success(f"Last saved receipt: #{last_receipt_id}")

    sale_date = st.date_input("Sale date", key="sale_date")

    products = connection.execute(
        "SELECT product_id, product_name, price_cents "
        "FROM products ORDER BY product_name"
    ).fetchall()

    product_column, summary_column = st.columns(2)
    sale_items = []
    receipt_rows = []
    total_cents = 0

    with product_column:
        for product_id, product_name, price_cents in products:
            quantity = st.number_input(
                f"{product_name} (${price_cents / 100:.2f} each)",
                min_value=0,
                step=1,
                key=f"quantity_{order_number}_{product_id}",
            )

            if quantity > 0:
                line_total_cents = quantity * price_cents
                total_cents += line_total_cents

                sale_items.append((product_id, quantity, price_cents))
                receipt_rows.append({
                    "Item": product_name,
                    "Qty": quantity,
                    "Amount": f"${line_total_cents / 100:.2f}",
                })

    with summary_column:
        st.subheader("Order summary")

        if receipt_rows:
            st.table(receipt_rows)
        else:
            st.caption("Add a quantity to start the order.")

        st.metric("Receipt total", f"${total_cents / 100:.2f}")

        if st.button("Save sale", type="primary", disabled=not sale_items):
            try:
                # Save the receipt and its items together.
                with connection:
                    receipt = connection.execute(
                        "INSERT INTO sales (sale_date) VALUES (?)",
                        (sale_date.isoformat(),),
                    )
                    sale_id = receipt.lastrowid

                    for product_id, quantity, price_cents in sale_items:
                        connection.execute(
                            "INSERT INTO sale_items "
                            "(sale_id, product_id, quantity, unit_price_cents) "
                            "VALUES (?, ?, ?, ?)",
                            (sale_id, product_id, quantity, price_cents),
                        )
            except sqlite3.Error as error:
                st.error(f"Could not save the sale. {error}")
            else:
                st.session_state["last_receipt_id"] = sale_id
                st.session_state["order_number"] = order_number + 1
                connection.close()
                st.rerun()

# Sales Report
with report_tab:
    monthly_query = (project_folder / "monthly_revenue.sql").read_text(
        encoding="utf-8-sig"
    )
    product_query = (project_folder / "product_sales_by_month.sql").read_text(
        encoding="utf-8-sig"
    )

    monthly_results = connection.execute(monthly_query).fetchall()

    if not monthly_results:
        st.info("Record a sale to see your first monthly report.")
        connection.close()
        st.stop()

    revenue_by_month = dict(monthly_results)
    available_months = sorted(revenue_by_month, reverse=True)
    selected_month = st.selectbox("Report month", available_months)

    monthly_revenue_cents = revenue_by_month[selected_month]
    product_results = connection.execute(
        product_query, (selected_month,)
    ).fetchall()

    receipt_count = connection.execute(
        """
        SELECT COUNT(*)
        FROM sales
        WHERE SUBSTR(sale_date, 1, 7) = ?
        """,
        (selected_month,),
    ).fetchone()[0]

    total_units_sold = 0
    product_rows = []
    chart_rows = []

    csv_file = StringIO()
    writer = csv.writer(csv_file)
    writer.writerow(["Product", "Units sold", "Revenue (USD)"])

    for product_name, units_sold, revenue_cents in product_results:
        total_units_sold += units_sold
        revenue_dollars = revenue_cents / 100

        product_rows.append({
            "Product": product_name,
            "Units sold": units_sold,
            "Revenue": f"${revenue_dollars:.2f}",
        })
        chart_rows.append({
            "Product": product_name,
            "Revenue (USD)": revenue_dollars,
        })
        writer.writerow([product_name, units_sold, f"{revenue_dollars:.2f}"])

    revenue_column, receipts_column, units_column = st.columns(3)
    revenue_column.metric("Revenue", f"${monthly_revenue_cents / 100:.2f}")
    receipts_column.metric("Receipts", receipt_count)
    units_column.metric("Items sold", total_units_sold)

    if chart_rows:
        st.subheader("Revenue by product")
        st.bar_chart(
            chart_rows,
            x="Product",
            y="Revenue (USD)",
            horizontal=True,
            color="#805137",
        )

    st.subheader("Product sales")
    st.table(product_rows)

    st.download_button(
        "Download product sales CSV",
        data=csv_file.getvalue(),
        file_name=f"product_sales_{selected_month}.csv",
        mime="text/csv",
    )

    # Show one row per receipt for the selected month.
    receipt_results = connection.execute(
        """
        SELECT
            sales.sale_id,
            sales.sale_date,
            SUM(sale_items.quantity) AS items_sold,
            SUM(sale_items.quantity * sale_items.unit_price_cents) AS total_cents
        FROM sales
        JOIN sale_items ON sales.sale_id = sale_items.sale_id
        WHERE SUBSTR(sales.sale_date, 1, 7) = ?
        GROUP BY sales.sale_id, sales.sale_date
        ORDER BY sales.sale_date DESC, sales.sale_id DESC
        """,
        (selected_month,),
    ).fetchall()

    receipt_history = []

    for sale_id, sale_date, items_sold, total_cents in receipt_results:
        receipt_history.append({
            "Receipt": f"#{sale_id}",
            "Date": sale_date,
            "Items": items_sold,
            "Total": f"${total_cents / 100:.2f}",
        })

    st.subheader("Receipts")
    st.table(receipt_history)

connection.close()