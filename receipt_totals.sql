SELECT
    sale_id,
    SUM(quantity * unit_price_cents) AS total_cents
FROM sale_items
GROUP BY sale_id
ORDER BY sale_id;