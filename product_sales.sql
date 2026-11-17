SELECT
	products.product_name,
	SUM(sale_items.quantity) AS units_sold,
	SUM(sale_items.quantity * sale_items.unit_price_cents) AS revenue_cents
FROM sale_items
JOIN products
	ON sale_items.product_id = products.product_id
GROUP BY products.product_id, products.product_name
ORDER BY units_sold DESC, products.product_name;