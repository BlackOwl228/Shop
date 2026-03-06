from datetime import datetime

from pydantic import BaseModel, ConfigDict


class StandartUserResponse(BaseModel):
    id: int
    name: str
    avatar: str | None


class ReviewResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    author: StandartUserResponse
    rating: int
    text: str | None
    image: str | None
    created_at: datetime


class ReviewsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    reviews: list[ReviewResponse]
    has_more: bool
