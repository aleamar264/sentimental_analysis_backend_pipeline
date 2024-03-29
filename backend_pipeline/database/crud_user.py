from copy import deepcopy
from fastapi.responses import JSONResponse
from pydantic import SecretStr
from model.user import User
from sqlalchemy import select, update, delete
from schemas.user_schema import (
    CreateUserSchema,
    ExtraUserInfoModel,
    ResponseUserSchema,
)
from typing import Any
from utils.fastapi.auth.dependencies import db_dependency
from utils.fastapi.auth.utils import hash_password


async def add_user(user: CreateUserSchema, db: db_dependency) -> User:
    _user = deepcopy(user.model_dump())
    _password: SecretStr = _user.pop("password1")
    del _user["password2"]
    hashed_password_ = hash_password(_password.get_secret_value())
    _user["password"] = hashed_password_
    stmt = User(**_user)
    db.add(stmt)
    db.commit()

    return stmt


async def modify_user(
    user_id: int, user: ExtraUserInfoModel, db: db_dependency
) -> ResponseUserSchema | JSONResponse:
    stmt = update(User).where(User.id == user_id).values(**user.model_dump())
    db.execute(stmt)
    db.commit()

    return get_user(user_id, db)


async def get_user(
    user_id: int, db: db_dependency
) -> ResponseUserSchema | JSONResponse:
    stmt = select(User).where(User.id == user_id)
    if (result := db.execute(stmt).scalars().one_or_none()) is None:
        return JSONResponse({"message": "User not found"}, status_code=404)
    result = result.__dict__
    del result["password"]
    response_ = ResponseUserSchema(**result)
    return response_


async def delete_user(user_id: int, db: db_dependency) -> JSONResponse:
    stmt = delete(User).where(User.id == user_id)
    db.execute(stmt)
    db.commit()

    return JSONResponse(
        {"message": "User deleted successfully"}, status_code=204
    )


async def get_all_users(db: db_dependency) -> list[ResponseUserSchema]:
    stmt = select(User)
    users = db.execute(stmt).scalars().all()
    if not users:
        return []
    users = [user.__dict__ for user in users]
    users = [remove_password(user) for user in users]
    return [ResponseUserSchema(**user) for user in users]


def remove_password(user: dict[str, Any]) -> dict[str, Any]:
    del user["password"]
    return user
