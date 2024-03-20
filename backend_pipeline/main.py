from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from utils.middleware import log_middleware


app = FastAPI()

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
app.openapi_url = "/docs"


@app.get("/health", status_code=200)
def status_health():
    return JSONResponse({"message": "OK!"}, status_code=status.HTTP_200_OK)
