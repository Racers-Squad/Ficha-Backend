-- alter card id name
-- depends: 20230825_07_QToxI-alter-currency-column-type
ALTER TABLE wallets RENAME COLUMN card_id TO id;
