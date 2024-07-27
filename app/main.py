from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from slowapi import _rate_limit_exceeded_handler
from middlewares.i18n import I18nMiddleware
from routers.auth import router as AuthRouter
from routers.roles import router as RoleRouter
from routers.users import router as UserRouter
from dependencies.slowapi_init import limiter
from dependencies.timezone_init import *
from enums.storage_path import StoragePath

# Create tables and seeders data
from migrations import role_table, user_table
from seeders import roles, users

app = FastAPI()

app.add_middleware(I18nMiddleware)

app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

app.mount("/avatar", StaticFiles(directory=StoragePath.AVATARS.value), name="avatar")
app.mount(
    "/static", StaticFiles(directory=StoragePath.STATIC_IMAGES.value), name="static"
)


app.include_router(AuthRouter)
app.include_router(UserRouter)
app.include_router(RoleRouter)
