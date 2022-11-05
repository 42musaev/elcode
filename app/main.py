from fastapi import FastAPI

from app.database.conf import database
from app.users.api import users

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(users)
