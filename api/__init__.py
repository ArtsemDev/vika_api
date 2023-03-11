from fastapi import APIRouter

from .v1 import v1_router
from .auth import auth_router

api_router = APIRouter(prefix='/api')
api_router.include_router(router=v1_router)
api_router.include_router(router=auth_router)
