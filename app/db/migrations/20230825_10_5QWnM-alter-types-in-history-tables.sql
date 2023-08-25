-- alter types in history tables
-- depends: 20230825_09_rMmjy-alter-tables-for-history

ALTER TABLE history_operations ALTER COLUMN start_meaning SET DATA TYPE int;
ALTER TABLE history_operations ALTER COLUMN operating SET DATA TYPE int;
ALTER TABLE history_operations ALTER COLUMN finish_meaning SET DATA TYPE int;
ALTER TABLE history_operations RENAME COLUMN operating TO value;
