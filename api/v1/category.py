from fastapi import APIRouter, status, Query, HTTPException
from slugify import slugify
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from core.models import Category
from core.schemas import CategorySchema, CategoryDBSchema

category_router = APIRouter(prefix='/category')


@category_router.post('/', response_model=CategoryDBSchema, status_code=status.HTTP_201_CREATED)
async def create_category(category: CategorySchema):
    obj = Category(
        name=category.name,
        slug=slugify(category.name)
    )
    try:
        await obj.save()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='category name is not unique')
    else:
        return CategoryDBSchema.from_orm(obj)


@category_router.get('/', response_model=list[CategoryDBSchema])
async def category_list():
    return [
        CategoryDBSchema.from_orm(obj)
        for obj in await Category.scalars(
            select(Category).order_by(Category.id.asc())
        )
    ]


@category_router.get('/{category_id}', response_model=CategoryDBSchema)
async def get_category(
        category_id: int = Query(
            ge=1,
            title='Category ID',
            description='Category unique ID'
        )
):
    obj = await Category.get(category_id)
    if obj:
        return CategoryDBSchema.from_orm(obj)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='category not found')


@category_router.delete('/{category_id}')
async def delete_category(
        category_id: int = Query(
            ge=1,
            title='Category ID',
            description='Category unique ID'
        )
):
    obj = await Category.get(category_id)
    if obj:
        await obj.delete()
        raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail='category delete successfully')
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='category not found')


@category_router.put('/', response_model=CategoryDBSchema, status_code=status.HTTP_202_ACCEPTED)
async def update_category(category: CategoryDBSchema):
    obj = await Category.get(category.id)
    if obj:
        obj.from_pydantic(schema=category)
        try:
            await obj.save()
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='category name is not unique')
        else:
            return category
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='category not found')
