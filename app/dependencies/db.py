from typing import AsyncGenerator, Type, Callable

from asyncpg import Pool, Connection
from fastapi import Depends
from fastapi.requests import Request

from app.db import BaseRepository


def _get_db_pool(request: Request) -> Pool:
    return request.app.state.db_pool


async def _get_connection_from_pool(
        pool: Pool = Depends(_get_db_pool),
) -> AsyncGenerator[Connection, None]:
    async with pool.acquire() as conn:
        yield conn


def get_repository(
        repo_type: Type[BaseRepository],
) -> Callable[[Connection], BaseRepository]:
    def _get_repo(
            conn: Connection = Depends(_get_connection_from_pool),
    ) -> BaseRepository:
        return repo_type(conn)

    return _get_repo
