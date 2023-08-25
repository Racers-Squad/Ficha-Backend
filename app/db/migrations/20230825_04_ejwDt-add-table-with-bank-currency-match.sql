-- add table with bank currencu match
-- depends: 20230825_03_U0uFz-add-currency-table
CREATE TABLE IF NOT EXISTS bank_currency_match(
    id serial primary key NOT NULL,
    bank_id int NOT NULL,
    currency_id int NOT NULL,
    FOREIGN KEY (bank_id) REFERENCES banks(id) ON DELETE CASCADE,
    FOREIGN KEY (currency_id) REFERENCES currencies(id) ON DELETE CASCADE
);
