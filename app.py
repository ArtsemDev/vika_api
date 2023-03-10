from fastapi import FastAPI

from api import api_router

app = FastAPI()
app.include_router(router=api_router)
