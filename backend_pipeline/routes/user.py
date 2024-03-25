from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from schemas.auth_schemas import CreateUserSchema  # type: ignore
from database.crud_user import add_user, get_user

# Create a new user

router = APIRouter(prefix="/users")


@router.get("/")
async def get_users():
    # TODO: get_user
    return {"users": ["Alice", "Bob", "Carol"]}


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateUserSchema,
    response_model_exclude={"password1", "password2"},
)
async def create_user(body: CreateUserSchema):
    return JSONResponse({"user": body})
