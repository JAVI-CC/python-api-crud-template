from fastapi import FastAPI, Depends, Request
from middlewares.i18n import I18nMiddleware
from routers.users import router as UserRouter
from routers.roles import router as RoleRouter
from routers.auth import router as AuthRouter
from migrations import *
from seeders import *
from fastapi.staticfiles import StaticFiles
from enums.storage_path import StoragePath
from dependencies.timezone_init import *
from slowapi import _rate_limit_exceeded_handler
from dependencies.slowapi_init import limiter

app = FastAPI()

app.add_middleware(I18nMiddleware)

app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

app.mount("/avatar", StaticFiles(directory=StoragePath.AVATARS.value), name="avatar")
app.mount("/static", StaticFiles(directory=StoragePath.STATIC_IMAGES.value), name="static")


app.include_router(AuthRouter)
app.include_router(UserRouter)
app.include_router(RoleRouter)
