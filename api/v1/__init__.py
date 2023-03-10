from fastapi import APIRouter

from .category import category_router


v1_router = APIRouter(prefix='/v1')
v1_router.include_router(router=category_router)
