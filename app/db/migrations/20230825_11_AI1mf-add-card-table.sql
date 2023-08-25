-- add card table
-- depends: 20230825_10_5QWnM-alter-types-in-history-tables

CREATE TABLE IF NOT EXISTS cards(
    id serial PRIMARY KEY NOT NULL,
    wallet_id int NOT NULL,
    user_id int NOT NULL,
    card_number int NOT NULL,
    expiration_time TIMESTAMP NOT NULL,
    FOREIGN KEY (wallet_id) REFERENCES wallets(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);