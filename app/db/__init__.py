from typing import AsyncGenerator, Type, Callable, List, Any

from asyncpg import Pool, Connection
from asyncpg.transaction import Transaction
from fastapi import Depends
from fastapi.requests import Request
from pydantic import BaseModel


class BaseRepository:
    def __init__(self, connection):
        self.connection: Connection = connection

    @property
    def transaction(self) -> Transaction:
        return self.connection.transaction()

    async def fetch_rows(self, query: str, *args, serializer: Type[BaseModel] = BaseModel) -> List[Any]:
        try:
            result = await self.connection.fetch(query, *args)
            if not result:
                return []
            result = list(map(lambda x: serializer.construct(**dict(x.items())), result))  # noqa
            return result
        except Exception as e:
            raise SQLException(e)

    async def fetch_one(self, query: str, *args, serializer: Type[BaseModel] = BaseModel) -> Any:
        try:
            result = await self.connection.fetchrow(query, *args)
            if not result:
                return None
            result = serializer.construct(**dict(result.items()))  # noqa
            return result
        except Exception as e:
            raise SQLException(e)


class SQLException(Exception):
    pass

