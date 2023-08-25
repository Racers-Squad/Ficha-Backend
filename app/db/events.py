import os

import asyncpg
from fastapi import FastAPI
from loguru import logger

from app.config import Config


async def connect_to_db(app: FastAPI, config: Config) -> None:
    logger.info("Connecting to PostgreSQL")
    dsn = get_dsn(config.db)
    app.state.db_pool = await asyncpg.create_pool(
        dsn=dsn,
        min_size=config.db.pool_min_size,
        max_size=config.db.pool_max_size,
    )

    logger.info("Connection established")


async def close_db_connection(app: FastAPI) -> None:
    logger.info("Closing connection to database")

    await app.state.db_pool.close()

    logger.info("Connection closed")


def get_dsn(config: Config) -> str:
    password = config.password or os.environ.get("DB_PASSWORD")
    user = config.user or os.environ.get("DB_USER")
    database = config.database or os.environ.get("DB_NAME")
    host = (config.host or os.environ.get("DB_HOST")) or "localhost"
    port = (config.port or os.environ.get("DB_PORT")) or 5432
    return f"postgres://{user}:{password}@{host}:{port}/{database}"
