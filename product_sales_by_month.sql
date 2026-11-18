SELECT
    products.product_name,
    SUM(sale_items.quantity) AS units_sold,
    SUM(sale_items.quantity * sale_items.unit_price_cents) AS revenue_cents
FROM sale_items
JOIN products ON sale_items.product_id = products.product_id
JOIN sales ON sale_items.sale_id = sales.sale_id
WHERE SUBSTR(sales.sale_date, 1, 7) = ?
GROUP BY products.product_id, products.product_name
ORDER BY revenue_cents DESC, products.product_name;