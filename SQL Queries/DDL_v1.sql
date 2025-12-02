CREATE SCHEMA IF NOT EXISTS app_schema;

CREATE TABLE app_schema.application_user (
  user_id uuid PRIMARY KEY,
  first_name varchar(100),
  last_name varchar(100),
  login_email varchar(150) UNIQUE,
  parser_email varchar(150) UNIQUE,
  fcm_token varchar(255),
  stripe_customer_id varchar(255) UNIQUE,
  created_at timestamp DEFAULT now(),
  timezone varchar(50),
  notification_threshold numeric(5,2) DEFAULT 10,
  plan_name varchar(50),
  plan_status varchar(50),
  current_period_start timestamp,
  current_period_end timestamp,
  plan_cancelled_on timestamp
);

CREATE TABLE app_schema.merchant (
  merchant_id uuid PRIMARY KEY,
  merchant_name varchar(100),
  url varchar(255),
  price_adjustment_window_days int DEFAULT 14,
  timezone varchar(50)
);

CREATE TABLE app_schema.transaction (
  transaction_id uuid PRIMARY KEY,
  user_id uuid,
  merchant_id uuid,
  transaction_date timestamp,
  transaction_amount numeric(10,2),
  transaction_savings_amount numeric(10,2),
  transaction_savings_percentage numeric(5,2),
  price_tracking_end_date timestamp,
  price_adjustment_days_left int,
  status varchar(50),
  created_at timestamp DEFAULT now()
);

CREATE TABLE app_schema.item (
  item_id uuid PRIMARY KEY,
  transaction_id uuid,
  product_id uuid,
  sku varchar(100),
  quantity int,
  purchase_price numeric(10,2),
  total_purchase_price numeric(10,2),
  lowest_price numeric(10,2),
  total_lowest_price numeric(10,2),
  price_difference_amount numeric(10,2),
  total_price_difference_amount numeric(10,2),
  price_difference_percentage numeric(5,2),
  lowest_price_timestamp timestamp
);

CREATE TABLE app_schema.product (
  product_id uuid PRIMARY KEY,
  merchant_id uuid,
  sku varchar(100),
  title varchar(255),
  fetch_url varchar(255),
  fetched_at timestamp,
  last_price numeric(10,2),
  status varchar(50)
);

CREATE TABLE app_schema.notification (
  notification_id uuid PRIMARY KEY,
  user_id uuid,
  payload text,
  fcm_message_id varchar(255) UNIQUE,
  status varchar(50),
  created_at timestamp DEFAULT now(),
  last_attempt_at timestamp,
  last_error_message text
);

ALTER TABLE app_schema.transaction
  ADD FOREIGN KEY (user_id) REFERENCES app_schema.application_user (user_id);
ALTER TABLE app_schema.transaction
  ADD FOREIGN KEY (merchant_id) REFERENCES app_schema.merchant (merchant_id);
ALTER TABLE app_schema.item
  ADD FOREIGN KEY (transaction_id) REFERENCES app_schema.transaction (transaction_id);
ALTER TABLE app_schema.item
  ADD FOREIGN KEY (product_id) REFERENCES app_schema.product (product_id);
ALTER TABLE app_schema.product
  ADD FOREIGN KEY (merchant_id) REFERENCES app_schema.merchant (merchant_id);
ALTER TABLE app_schema.notification
  ADD FOREIGN KEY (user_id) REFERENCES app_schema.application_user (user_id);