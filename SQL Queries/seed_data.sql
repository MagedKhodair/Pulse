-- Insert 3 items with seed data
INSERT INTO app_schema.item (
  item_id,
  transaction_id,
  product_id,
  sku,
  quantity,
  purchase_price,
  lowest_price,
  lowest_price_timestamp
) VALUES
-- Item 1
(
  gen_random_uuid(),
  'TRANS001',
  'PROD001',
  'SKU-12345',
  1,
  49.99,
  39.99,
  NOW() + INTERVAL '2 days'
),
-- Item 2
(
  gen_random_uuid(),
  'TRANS001',
  'PROD002',
  'SKU-67890',
  2,
  29.99,
  24.99,
  NOW() + INTERVAL '3 days'
),
-- Item 3
(
  gen_random_uuid(),
  'TRANS001',
  'PROD003',
  'SKU-11111',
  3,
  15.50,
  12.50,
  NOW() + INTERVAL '1 day'
);


-- Insert a product with seed data
-- Insert 3 products matching the items
INSERT INTO app_schema.product (
  product_id,
  merchant_id,
  sku,
  title,
  fetch_url,
  fetched_at,
  last_price,
  status
) VALUES
-- Product 1 (matches Item 1)
(
  'PROD001',
  'MERCH001',
  'SKU-12345',
  'Wireless Headphones',
  'https://amazon.com/wireless-headphones',
  NOW(),
  39.99,
  'active'
),
-- Product 2 (matches Item 2)
(
  'PROD002',
  'MERCH001',
  'SKU-67890',
  'USB-C Cable 2Pack',
  'https://amazon.com/usb-c-cable',
  NOW(),
  24.99,
  'active'
),
-- Product 3 (matches Item 3)
(
  'PROD003',
  'MERCH001',
  'SKU-11111',
  'Phone Case',
  'https://amazon.com/phone-case',
  NOW(),
  12.50,
  'active'
);

-- Insert 1 merchant
INSERT INTO app_schema.merchant (
  merchant_id,
  merchant_name,
  url,
  price_adjustment_window_days,
  timezone
) VALUES
(
  'MERCH001',
  'Amazon',
  'https://amazon.com',
  14,
  'UTC'
);

-- Insert a transaction with seed data
INSERT INTO app_schema.transaction (
  transaction_id,
  user_id,
  merchant_id,
  transaction_date,
  transaction_amount,
  transaction_savings_amount,
  price_tracking_end_date
) VALUES
(
  'TRANS001',               -- transaction_id
  'nauvowHUHuhBzyJinRzbe0nKf6e2',                -- user_id (replace with actual user_id)
  'MERCH001',               -- merchant_id (linked to the merchant you created earlier)
  NOW(),                    -- transaction_date (current timestamp)
  100.00,                   -- transaction_amount
  10.00,                    -- transaction_savings_amount
  NOW() + INTERVAL '14 days' -- price_tracking_end_date (14 days from now)
);

INSERT INTO app_schema.application_user (
    user_id,
    first_name,
    last_name,
    login_email
) VALUES (
    'nauvowHUHuhBzyJinRzbe0nKf6e2',
    'Tyler',
    'Durden',
    'tyler.durden@gmail.com'
);

--
UPDATE app_schema.transaction
SET item_count = 6
WHERE transaction_id = 'TRANS001';