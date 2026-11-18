# Café Sales Dashboard

A Streamlit app for recording sales and reviewing monthly performance at a fictional café. I built it with Python, Streamlit, and SQLite to practice connecting a sales entry form to a database and using SQL to turn those records into reports.

## Features

### Record a Sale

- Choose a sale date and enter the quantity for each product.
- Review the items, prices, and total before saving.
- Save the sale to SQLite and see the receipt number.

### Sales Report

- Select a month to see revenue, receipt count, and items sold.
- Compare product revenue in a bar chart and review quantities in the product table.
- View individual receipts for the selected month.
- Download the monthly product sales report as a CSV file for Excel.

## Run the app locally

Download or clone this repository. Open the project folder in VS Code and run these commands in the terminal:

```powershell
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

Open the **Local URL** shown in the terminal. The app can start in demo mode using the fictional records in `sample_data.sql`. Sales entered in demo mode are saved for the current session.

## Try it

1. Open **Record a Sale** and enter one iced coffee and two croissants.
2. Confirm the total is **$6.00**, then save the sale.
3. Open **Sales Report**, select the month of the sale, and find the new receipt.
4. Download the product sales CSV and compare it with the table on screen.

## Future improvements

- Track stock levels and flag low-stock products.
- Record product costs to calculate gross profit.
