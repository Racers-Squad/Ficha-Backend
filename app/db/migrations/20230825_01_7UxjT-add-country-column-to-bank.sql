-- add country column to bank
-- depends: 20230824_03_twbhg-alter-mail-column-name
ALTER TABLE banks ADD COLUMN country text NOT NULL;
