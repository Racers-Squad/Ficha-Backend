-- initial-tables
-- depends: 
CREATE TABLE "users" (
	"id" serial UNIQUE,
	"name" VARCHAR(255),
	"surname" VARCHAR(255),
	"mail" VARCHAR(255),
	"password" VARCHAR(255),
	"phone" VARCHAR(255),
	"role" integer,
	CONSTRAINT "users_pk" PRIMARY KEY ("id")
);



CREATE TABLE "wallets" (
	"user_id" integer,
	"card_id" serial UNIQUE,
	"currency" VARCHAR(255),
	"score" integer,
	"credit_rating" integer,
	"bank" integer,
	CONSTRAINT "wallets_pk" PRIMARY KEY ("card_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "history_operations" (
	"id" serial UNIQUE,
	"card_id" integer,
	"start_meaning" FLOAT,
	"operating" FLOAT,
	"type_operation" integer,
	"finish_meaning" FLOAT,
	CONSTRAINT "history_operations_pk" PRIMARY KEY ("id")
);



CREATE TABLE "banks" (
	"id" serial UNIQUE,
	"bank" VARCHAR(255) UNIQUE,
	CONSTRAINT "BANKS_pk" PRIMARY KEY ("id")
);



CREATE TABLE "type_operation" (
	"id" serial UNIQUE,
	"operating" VARCHAR(255) UNIQUE,
	CONSTRAINT "type_operation_pk" PRIMARY KEY ("id")
);




ALTER TABLE "wallets" ADD CONSTRAINT "wallets_fk0" FOREIGN KEY ("user_id") REFERENCES "users"("id");
ALTER TABLE "wallets" ADD CONSTRAINT "wallets_fk1" FOREIGN KEY ("bank") REFERENCES "banks"("id");

ALTER TABLE "history_operations" ADD CONSTRAINT "history_operations_fk0" FOREIGN KEY ("card_id") REFERENCES "wallets"("card_id");
ALTER TABLE "history_operations" ADD CONSTRAINT "history_operations_fk1" FOREIGN KEY ("type_operation") REFERENCES "type_operation"("id");
