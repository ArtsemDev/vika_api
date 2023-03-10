from pydantic import BaseModel, Field, root_validator
from slugify import slugify


class CategorySchema(BaseModel):
    name: str = Field(
        min_length=4,
        max_length=64,
        title='Category name',
        description='Category name'
    )


class CategoryDBSchema(CategorySchema):
    id: int = Field(
        ge=1,
        title='Category ID',
        description='Category unique ID'
    )
    slug: str = Field(
        min_length=4,
        max_length=64,
        title='Category URL',
        description='Category URL',
        default=None
    )

    @root_validator
    def validator(cls, values: dict) -> dict:
        if not values.get('slug'):
            values['slug'] = slugify(values.get('name'))
        return values
