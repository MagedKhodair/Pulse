-- Drop foreign key constraints first
ALTER TABLE app_schema.notification
DROP CONSTRAINT notification_user_id_fkey;

ALTER TABLE app_schema.product
DROP CONSTRAINT product_merchant_id_fkey;

ALTER TABLE app_schema.item
DROP CONSTRAINT item_product_id_fkey;

ALTER TABLE app_schema.item
DROP CONSTRAINT item_transaction_id_fkey;

ALTER TABLE app_schema.transaction
DROP CONSTRAINT transaction_merchant_id_fkey;

ALTER TABLE app_schema.transaction
DROP CONSTRAINT transaction_user_id_fkey;

-- Now alter the columns from uuid to VARCHAR(50)
ALTER TABLE app_schema.application_user
ALTER COLUMN user_id TYPE VARCHAR(50);

ALTER TABLE app_schema.merchant
ALTER COLUMN merchant_id TYPE VARCHAR(50);

ALTER TABLE app_schema.transaction
ALTER COLUMN transaction_id TYPE VARCHAR(50),
ALTER COLUMN user_id TYPE VARCHAR(50),
ALTER COLUMN merchant_id TYPE VARCHAR(50);

ALTER TABLE app_schema.item
ALTER COLUMN item_id TYPE VARCHAR(50),
ALTER COLUMN transaction_id TYPE VARCHAR(50),
ALTER COLUMN product_id TYPE VARCHAR(50);

ALTER TABLE app_schema.product
ALTER COLUMN product_id TYPE VARCHAR(50),
ALTER COLUMN merchant_id TYPE VARCHAR(50);

ALTER TABLE app_schema.notification
ALTER COLUMN notification_id TYPE VARCHAR(50),
ALTER COLUMN user_id TYPE VARCHAR(50);

-- Recreate the foreign key constraints
ALTER TABLE app_schema.transaction
ADD CONSTRAINT transaction_user_id_fkey FOREIGN KEY (user_id) REFERENCES app_schema.application_user (user_id),
ADD CONSTRAINT transaction_merchant_id_fkey FOREIGN KEY (merchant_id) REFERENCES app_schema.merchant (merchant_id);

ALTER TABLE app_schema.item
ADD CONSTRAINT item_transaction_id_fkey FOREIGN KEY (transaction_id) REFERENCES app_schema.transaction (transaction_id),
ADD CONSTRAINT item_product_id_fkey FOREIGN KEY (product_id) REFERENCES app_schema.product (product_id);

ALTER TABLE app_schema.product
ADD CONSTRAINT product_merchant_id_fkey FOREIGN KEY (merchant_id) REFERENCES app_schema.merchant (merchant_id);

ALTER TABLE app_schema.notification
ADD CONSTRAINT notification_user_id_fkey FOREIGN KEY (user_id) REFERENCES app_schema.application_user (user_id);