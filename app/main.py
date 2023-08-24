import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRoute

from app.api.errors.db_error_handler import db_error_handler
from app.api.errors.http_error_handler import http_error_handler
from app.db import SQLException
from app.api.routes.api import router as api_router
from app.config import Config
from app.events import create_start_app_db_handler, create_stop_app_db_handler

config = Config()


def create_application() -> FastAPI:
    app = FastAPI(**config.app)  # noqa

    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.app.allowed_hosts,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )
    app.add_event_handler(
        "startup",
        create_start_app_db_handler(app, config),
    )
    app.add_event_handler(
        "shutdown",
        create_stop_app_db_handler(app),
    )

    app.add_exception_handler(HTTPException, http_error_handler)
    app.add_exception_handler(SQLException, db_error_handler)
    app.include_router(api_router, prefix=config.app.api_prefix)

    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name

    return app


app = create_application()

if __name__ == "__main__":
    uvicorn.run(app, host=config.app.host, port=config.app.port)
