-- delete bank column
-- depends: 20230825_05_0hOOE-rename-credit-rating-column

ALTER TABLE wallets DROP COLUMN bank;