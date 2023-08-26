-- alter type of expiration time
-- depends: 20230826_02_WXEjZ-add-bank-id-column
ALTER TABLE cards ALTER COLUMN expiration_time TYPE TIMESTAMP WITH TIME ZONE;
