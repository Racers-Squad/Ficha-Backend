-- rename credit rating column
-- depends: 20230825_04_ejwDt-add-table-with-bank-currency-match

ALTER TABLE wallets RENAME COLUMN credit_rating TO status;