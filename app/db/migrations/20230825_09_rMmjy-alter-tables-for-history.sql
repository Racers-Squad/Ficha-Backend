-- alter tables for history
-- depends: 20230825_08_513r2-alter-card-id-name

ALTER TABLE history_operations RENAME COLUMN card_id to wallet_id;
ALTER TABLE type_operation RENAME COLUMN operating to name;

INSERT INTO type_operation(id, name)
VALUES
    (1, 'REPLENISHMENT'),
    (2, 'WITHDRAWAL'),
    (3, 'TRANSFER');