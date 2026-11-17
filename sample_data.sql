-- Sample data for a fictional café.

INSERT INTO sales (sale_id, sale_date)
VALUES
    (101, '2026-11-17'),
    (102, '2026-11-17');

INSERT INTO products (product_id, product_name, price_cents)
VALUES
    ('P01', 'Iced Coffee', 250),
    ('P02', 'Croissant', 175);

INSERT INTO sale_items (sale_id, product_id, quantity, unit_price_cents)
VALUES
    (101, 'P01', 2, 250),
    (101, 'P02', 1, 175),
    (102, 'P01', 1, 250),
    (102, 'P02', 2, 175);