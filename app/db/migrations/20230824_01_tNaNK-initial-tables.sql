-- initial-tables
-- depends: 
CREATE TABLE "USERS" (
	"id" serial UNIQUE,
	"name" VARCHAR(255),
	"surname" VARCHAR(255),
	"mail" VARCHAR(255),
	"password" VARCHAR(255),
	"phone" VARCHAR(255),
	"role" integer,
	CONSTRAINT "USERS_pk" PRIMARY KEY ("id")
);



CREATE TABLE "WALLETS" (
	"user_id" integer,
	"card_id" serial UNIQUE,
	"currency" VARCHAR(255),
	"score" integer,
	"credit_rating" integer,
	"bank" integer,
	CONSTRAINT "WALLETS_pk" PRIMARY KEY ("card_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "HISTORYOPERATIONS" (
	"id" serial UNIQUE,
	"card_id" integer,
	"start_meaning" FLOAT,
	"operating" FLOAT,
	"type_operation" integer,
	"finish_meaning" FLOAT,
	CONSTRAINT "HISTORYOPERATIONS_pk" PRIMARY KEY ("id")
);



CREATE TABLE "BANKS" (
	"id" serial UNIQUE,
	"bank" VARCHAR(255) UNIQUE,
	CONSTRAINT "BANKS_pk" PRIMARY KEY ("id")
);



CREATE TABLE "TYPEOPERATIONENUM" (
	"id" serial UNIQUE,
	"operating" VARCHAR(255) UNIQUE,
	CONSTRAINT "TYPEOPERATIONENUM_pk" PRIMARY KEY ("id")
);




ALTER TABLE "WALLETS" ADD CONSTRAINT "WALLETS_fk0" FOREIGN KEY ("user_id") REFERENCES "USERS"("id");
ALTER TABLE "WALLETS" ADD CONSTRAINT "WALLETS_fk1" FOREIGN KEY ("bank") REFERENCES "BANKS"("id");

ALTER TABLE "HISTORYOPERATIONS" ADD CONSTRAINT "HISTORYOPERATIONS_fk0" FOREIGN KEY ("card_id") REFERENCES "WALLETS"("card_id");
ALTER TABLE "HISTORYOPERATIONS" ADD CONSTRAINT "HISTORYOPERATIONS_fk1" FOREIGN KEY ("type_operation") REFERENCES "TYPEOPERATIONENUM"("id");
