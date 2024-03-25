from model.user import User
from copy import deepcopy
from sqlalchemy import select, update, delete
from schemas.auth_schemas import CreateUserSchema
from utils.fastapi.auth.dependencies import db_dependency
from utils.fastapi.auth.utils import hash_password


def add_user(user: CreateUserSchema, db: db_dependency) -> User:
    _user = deepcopy(user.model_dump())
    _password = _user["password1"].pop()
    del _user["password2"]
    hashed_password_ = hash_password(_password)
    _user["password"] = hashed_password_
    stmt = User(**_user)
    db.add(stmt)
    db.commit()

    return stmt


def get_user(user_id: int, db: db_dependency) -> User | None:
    stmt = select(User).where(User.id == user_id)
    result = db.execute(stmt).scalars().one_or_none()
    return result
