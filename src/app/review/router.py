from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, Path, Query, UploadFile

from src.core.dependencies.services import get_review_service
from src.core.dependencies.users import get_current_user
from src.models.users import User
from src.services.media import delete_image, save_image
from src.services.review import ReviewService

from .schemas import ReviewsResponse

router = APIRouter(tags=["Review"])


@router.post("/products/{product_id}/reviews", status_code=201)
async def create_review(
    background_tasks: BackgroundTasks,
    product_id: int = Path(...),
    rating: int = Form(..., ge=1, le=5),
    text: str | None = Form(None, max_length=500),
    image: UploadFile | None = File(
        None, max_length=15 * 1024 * 1024, media_type=["image/png", "image/jpeg"]
    ),
    author: User = Depends(get_current_user),
    review_service: ReviewService = Depends(get_review_service),
):
    review = review_service.create_review(
        author_id=author.id, product_id=product_id, rating=rating, text=text, image=image
    )

    if image is not None:
        background_tasks.add_task(save_image, image, review.image)

    return {"status": "Review created", "review_id": review.id}


@router.get("/products/{product_id}/reviews", response_model=ReviewsResponse)
def get_product_reviews(
    product_id: int = Path(...),
    page: int = Query(1, ge=1),
    size: int = Query(20, le=50),
    review_service: ReviewService = Depends(get_review_service),
):
    reviews, has_more = review_service.get_reviews_to_product(product_id=product_id, page=page, size=size)

    return {"reviews": reviews[:size], "has_more": has_more}


@router.patch("/reviews/{review_id}", status_code=204)
def edit_review(
    background_tasks: BackgroundTasks,
    review_id: int = Path(...),
    rating: int | None = Form(None, ge=1, le=5),
    text: str | None = Form(None, max_length=500),
    image: UploadFile | None = File(
        None, max_length=15 * 1024 * 1024, media_type=["image/png", "image/jpeg"]
    ),
    author: User = Depends(get_current_user),
    review_service: ReviewService = Depends(get_review_service),
):
    review = review_service.change_review(
        author_id=author.id, review_id=review_id, rating=rating, text=text, image=image
    )

    if image is not None:
        background_tasks.add_task(save_image, image, review.image)


@router.delete("/reviews/{review_id}", status_code=204)
def delete_review(
    background_tasks: BackgroundTasks,
    review_id: int = Path(...),
    author: User = Depends(get_current_user),
    review_service: ReviewService = Depends(get_review_service),
):
    image_path = review_service.delete_review(author_id=author.id, review_id=review_id)

    if image_path:
        background_tasks.add_task(delete_image, image_path)
