-- change name column in bank
-- depends: 20230825_01_7UxjT-add-country-column-to-bank
ALTER TABLE banks RENAME COLUMN bank TO name;
