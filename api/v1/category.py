from fastapi import APIRouter, status, Query, HTTPException

from core.schemas import CategorySchema, CategoryDBSchema


category_router = APIRouter(prefix='/category')
categories = []


@category_router.post('/', response_model=CategoryDBSchema, status_code=status.HTTP_201_CREATED)
async def create_category(category: CategorySchema):
    category_db = CategoryDBSchema(
        **category.dict() | {'id': len(categories) + 1}
    )
    categories.append(category_db)
    return category_db


@category_router.get('/', response_model=list[CategoryDBSchema])
async def category_list():
    return categories


@category_router.get('/{category_id}', response_model=CategoryDBSchema)
async def get_category(
        category_id: int = Query(
            ge=1,
            title='Category ID',
            description='Category unique ID'
        )
):
    obj = [*filter(lambda x: x.id == category_id, categories)]
    if obj:
        return obj[0]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='category not found')


@category_router.delete('/{category_id}')
async def delete_category(
        category_id: int = Query(
            ge=1,
            title='Category ID',
            description='Category unique ID'
        )
):
    for i, category in enumerate(categories):
        if category.id == category_id:
            del categories[i]
            raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail='Category delete successfully')
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not found')


@category_router.put('/{category_id}', response_model=CategoryDBSchema, status_code=status.HTTP_202_ACCEPTED)
async def edit_category(category: CategoryDBSchema):
    for i, obj in enumerate(categories):
        if obj.id == category.id:
            categories[i] = category
            return category
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='category not found')
