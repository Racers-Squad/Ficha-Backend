-- add currency table
-- depends: 20230825_02_ZemZp-change-name-column-in-bank

CREATE TABLE IF NOT EXISTS currencies(
        id serial PRIMARY KEY NOT NULL,
        name varchar(60) NOT NULL,
        short_name varchar(10) NOT NULL
);