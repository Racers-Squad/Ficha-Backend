-- add bank id column
-- depends: 20230826_01_X2Ef0-insert-currencies

ALTER TABLE cards ADD COLUMN bank_id int NOT NULL;