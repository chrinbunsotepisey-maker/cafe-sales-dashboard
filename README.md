# cafe-sales-dashboard
A café sales and inventory dashboard built with Python, SQL, and Streamlit.

I'm building a dashboard for a coffee shop to track sales, gross profit, and stock levels.

## Questions I want to answer

- How much revenue does the café earn each month?
- Which products sell the most, and which earn the most gross profit?
- Which products are running low on stock?

## Tools I plan to use

- SQLite and SQL for the database and analysis
- Python and Streamlit for the interactive dashboard

## Project status

The database schema, sample data, and receipt totals query are complete and tested in a fresh SQLite database.

## How to run the SQL example

1. Open DB Browser for SQLite and create a new, empty database.
2. In Execute SQL, run `schema.sql` to create the tables.
3. Run `sample_data.sql` to load the fictional café receipts.
4. Run `receipt_totals.sql` to calculate the total for each receipt.

Click **Write Changes** after steps 2 and 3 if the button is enabled.

### Expected results

| Receipt | Total (cents) | Total (USD) |
| --- | ---: | ---: |
| 101 | 675 | $6.75 |
| 102 | 600 | $6.00 |
