from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from utils.middleware import log_middleware  # type: ignore
from utils.database.general import _engine
from model.user import Base
from routes.user import router as user_route

Base.metadata.create_all(bind=_engine)

app = FastAPI(
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    root_path="/api/v1",
)

allow_origins = ["*"]
allow_methods = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=allow_methods,
    allow_headers=["*"],
)

app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)
app.include_router(user_route)


@app.get("/health", status_code=200)
def status_health():
    return JSONResponse({"message": "OK!"}, status_code=status.HTTP_200_OK)
