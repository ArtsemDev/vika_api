from fastapi import APIRouter

from .auth import auth

auth_router = APIRouter(prefix='/auth')
auth_router.include_router(router=auth)
