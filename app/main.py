from fastapi import FastAPI
from routers.users import router as UserRouter
from routers.roles import router as RoleRouter
from routers.auth import router as AuthRouter
from migrations import *
from seeders.init import *
from fastapi.staticfiles import StaticFiles
from enums.storage_path import StoragePath

app = FastAPI()

app.mount("/avatar", StaticFiles(directory=StoragePath.AVATARS.value), name="avatar")

app.include_router(AuthRouter)
app.include_router(UserRouter)
app.include_router(RoleRouter)
