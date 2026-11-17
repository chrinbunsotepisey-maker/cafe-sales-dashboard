SELECT 
	SUBSTR(sales.sale_date, 1, 7) AS sale_month,
	SUM(sale_items.quantity * sale_items.unit_price_cents) AS revenue_cents
FROM sales
JOIN sale_items
	ON sales.sale_id = sale_items.sale_id
GROUP BY sale_month
ORDER BY sale_month;