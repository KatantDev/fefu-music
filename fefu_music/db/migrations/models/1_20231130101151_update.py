from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "usermodel" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" TEXT NOT NULL,
    "avatar_url" TEXT NOT NULL,
    "email" VARCHAR(320) NOT NULL UNIQUE,
    "status" VARCHAR(5) NOT NULL  DEFAULT 'user',
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "usermodel"."status" IS 'USER: user\nADMIN: admin';
COMMENT ON TABLE "usermodel" IS 'Model for users.';
        CREATE TABLE IF NOT EXISTS "refreshtokenmodel" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "expires_at" TIMESTAMPTZ NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "user_id" UUID NOT NULL REFERENCES "usermodel" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "refreshtokenmodel" IS 'Model for refresh tokens.';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "usermodel";
        DROP TABLE IF EXISTS "refreshtokenmodel";"""
