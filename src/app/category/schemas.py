from pydantic import BaseModel, ConfigDict


class CategoryResponse(BaseModel):
    id: int
    name: str


class CategoriesPesponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    categories: list[CategoryResponse]
