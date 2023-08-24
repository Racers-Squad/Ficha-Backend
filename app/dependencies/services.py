from fastapi import Depends

from app.db.repositories.user import UserRepository
from app.dependencies.db import get_repository
from app.services.users import Users


def get_user_service(repo: UserRepository = Depends(get_repository(UserRepository))):
    return Users(repo)
