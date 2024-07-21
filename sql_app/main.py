from fastapi import FastAPI
from routers.users import router as UserRouter
from routers.roles import router as RoleRouter
from routers.auth import router as AuthRouter
from migrations.init import *
from seeders.init import *

app = FastAPI()

app.include_router(AuthRouter)
app.include_router(UserRouter)
app.include_router(RoleRouter)