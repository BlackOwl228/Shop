from fastapi import APIRouter, BackgroundTasks, UploadFile, Path, Depends, File, Form, Query
from core.media import save_image, delete_image
from services.review import ReviewService
from services.public import PublicService
from core.depends import get_review_service, get_public_service
from .schemas import ReviewsResponse
from ..search.schemas import OrderingParam

router = APIRouter(tags=["Review"])

@router.post('/products/{product_id}/reviews', status_code=201)
async def create_review(background_tasks: BackgroundTasks,
                        product_id: int = Path(...),
                        rating: int = Form(..., ge=1, le=5),
                        text: str | None = Form(None, max_length=500),
                        image: UploadFile | None = File(None, max_length=15 *1024*1024, media_type=['image/png', 'image/jpeg']),
                        review_service: ReviewService = Depends(get_review_service)):
    review, path = review_service.create_review(product_id=product_id, rating=rating, text=text, image=image)

    if path:
        background_tasks.add_task(save_image, image, path)

    return {"status": "Review created", "review_id": review.id}

@router.get('/products/{product_id}/reviews', response_model=ReviewsResponse)
def get_product_reviews(product_id: int = Path(...),
                        page: int = Query(1, ge=1),
                        size: int = Query(20, le=50),
                        order: OrderingParam = Query(OrderingParam.desc),
                        public_service: PublicService = Depends(get_public_service)):
    reviews, has_more = public_service.get_reviews_to_product(product_id=product_id, page=page, size=size, order=order)

    return {"reviews": reviews[:size], "has_more": has_more}

@router.patch('/reviews/{review_id}', status_code=204)
def edit_review(background_tasks: BackgroundTasks,
                review_id: int = Path(...),
                rating: int | None= Form(None, ge=1, le=5),
                text: str | None = Form(None, max_length=500),
                image: UploadFile | None = File(None, max_length=15 *1024*1024, media_type=['image/png', 'image/jpeg']),
                review_service: ReviewService = Depends(get_review_service)):
    path = review_service.change_review(review_id=review_id, rating=rating, text=text, image=image)

    if path:
        background_tasks.add_task(save_image, image, path)

@router.delete('/reviews/{review_id}', status_code=204)
def delete_review(review_id: int = Path(...),
                  review_service: ReviewService = Depends(get_review_service)):
    review_service.delete_review(review_id)