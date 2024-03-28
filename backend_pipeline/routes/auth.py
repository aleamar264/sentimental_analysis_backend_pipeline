from passlib.context import CryptContext
from fastapi import APIRouter
from schemas.user_schema import ResponseUserSchema
from schemas.auth_schema import Token
from fastapi.responses import JSONResponse
from fastapi import HTTPException, status
from utils.fastapi.auth.dependencies import (
    db_dependency,
    form_data,
    create_access_token,
)
from datetime import timedelta
from sqlalchemy import select
from model.user import User


router = APIRouter(prefix="/auth", tags=["auth"])

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def authenticated_user(
    username: str, password: str, db
) -> ResponseUserSchema | bool:
    stmt = select(User).filter(User.username == username)
    user: User | None = db.execute(stmt).scalar_one_or_none()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    _user = user.__dict__
    del _user["password"]
    return ResponseUserSchema(**_user)


@router.post("/token", response_model=Token)
async def login_for_access_token(form: form_data, db: db_dependency):
    user: ResponseUserSchema | bool = authenticated_user(
        form.username, form.password, db
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user.",
        )
    token = create_access_token(
        user.username, user.id, user.role.value, timedelta(minutes=20)
    )
    return JSONResponse(
        {"access_token": token, "token_type": "bearer"}, status_code=200
    )
