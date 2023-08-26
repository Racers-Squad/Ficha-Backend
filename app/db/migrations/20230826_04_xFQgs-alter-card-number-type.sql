-- alter card number type
-- depends: 20230826_03_kiJmd-alter-type-of-expiration-time

ALTER TABLE cards ALTER COLUMN card_number TYPE text;