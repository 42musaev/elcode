from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.conf import database
from app.users.api import users
from app.notes.api import notes

app = FastAPI(docs_url='/api/v1/docs', redoc_url='/api/v1/redoc')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost, http://localhost:3000'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(users, prefix='/api/v1')
app.include_router(notes, prefix='/api/v1')
