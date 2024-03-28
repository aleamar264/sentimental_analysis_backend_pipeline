from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from schemas.user_schema import (
    CreateUserSchema,
    ResponseUserSchema,
)  # type: ignore
from database.crud_user import add_user, delete_user, get_user, get_all_users
from utils.fastapi.auth.dependencies import db_dependency, user_dependency

ROUTE = "http://localhost:9000/api/v1"
ENDPOINT = "/users"

router = APIRouter(prefix=ENDPOINT, tags=["users"])


@router.get("/users", response_model=list[ResponseUserSchema])
async def get_users(
    db: db_dependency, user: user_dependency
) -> list[ResponseUserSchema] | JSONResponse:
    if user.get("user_role") != "admin":
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Unauthorized"},
        )
    return await get_all_users(db)


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(
    body: CreateUserSchema, db: db_dependency
) -> JSONResponse:
    _user = await add_user(body, db)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"url": f"{ROUTE}{ENDPOINT}/{_user.id}"},
    )


@router.get("/", response_model=ResponseUserSchema)
async def get_user_by_id(
    db: db_dependency, user: user_dependency
) -> ResponseUserSchema | JSONResponse:
    return await get_user(user["id"], db)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(
    db: db_dependency, user: user_dependency
) -> JSONResponse:
    return await delete_user(user["id"], db)
