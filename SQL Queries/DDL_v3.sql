ALTER TABLE app_schema.item
DROP COLUMN price_difference_amount;

ALTER TABLE app_schema.item
RENAME COLUMN price_difference_percentage TO total_price_difference_percentage;

-- For item table - add calculation logic to existing columns
ALTER TABLE app_schema.item
DROP COLUMN total_purchase_price,
DROP COLUMN total_lowest_price,
DROP COLUMN total_price_difference_amount,
DROP COLUMN total_price_difference_percentage;

ALTER TABLE app_schema.item
ADD COLUMN total_purchase_price numeric(10,2) GENERATED ALWAYS AS (purchase_price * quantity) STORED,
ADD COLUMN total_lowest_price numeric(10,2) GENERATED ALWAYS AS (lowest_price * quantity) STORED,
ADD COLUMN total_price_difference_amount numeric(10,2) GENERATED ALWAYS AS ((purchase_price - lowest_price) * quantity) STORED,
ADD COLUMN total_price_difference_percentage numeric(5,2) GENERATED ALWAYS AS (ROUND(((purchase_price - lowest_price) / purchase_price * 100), 2)) STORED;

--

ALTER TABLE app_schema.transaction
DROP COLUMN status;



--
ALTER TABLE app_schema.transaction
DROP COLUMN IF EXISTS price_adjustment_days_left;


--
ALTER TABLE app_schema.transaction
DROP COLUMN IF EXISTS created_at;

ALTER TABLE app_schema.transaction
ADD COLUMN created_at timestamptz DEFAULT CURRENT_TIMESTAMP;

--
ALTER TABLE app_schema.transaction
DROP COLUMN IF EXISTS transaction_savings_percentage;

ALTER TABLE app_schema.transaction
ADD COLUMN transaction_savings_percentage numeric(5,2) GENERATED ALWAYS AS (
  ROUND((transaction_savings_amount / NULLIF(transaction_amount, 0) * 100), 2)
) STORED;