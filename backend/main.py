import os

import icfpc2019.app as icfpc2019
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


@app.get("/api/v1/hello")
async def index():
    return {"message": "hello world!"}

@app.middleware("http")
async def auth_secret_token(request: Request, call_next):
    if os.getenv("PRODUCTION"):
        if ("X-Negainoido-Secret" not in request.headers or
           request.headers["X-Negainoido-Secret"] != os.getenv("SECRET_TOKEN")):
            return JSONResponse(content={"error": "Unauthorized"}, status_code=401)
    return await call_next(request)

app.include_router(icfpc2019.router, prefix="/api/v1/icfpc2019", tags=["icfpc2019"])

if not os.getenv("PRODUCTION"):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
