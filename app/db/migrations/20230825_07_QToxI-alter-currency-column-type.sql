-- alter currency column type
-- depends: 20230825_06_BaA3S-delete-bank-column
ALTER TABLE wallets ALTER COLUMN currency SET DATA TYPE int USING currency::integer;
