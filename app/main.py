from fastapi import FastAPI

from app.auth.routers import router as auth_router
from app.delivery.routers import router as dishes_router
from app.loggers import set_logger

app = FastAPI()

routers = [auth_router, dishes_router]


for router in routers:
    app.include_router(router)

set_logger(__name__)
