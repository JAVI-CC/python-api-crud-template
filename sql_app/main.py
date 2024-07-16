from fastapi import FastAPI
from routers.users import router as UserRouter
from routers.roles import router as RoleRouter

app = FastAPI()

app.include_router(UserRouter)
app.include_router(RoleRouter)
