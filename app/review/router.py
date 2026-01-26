import os

from fastapi import APIRouter, HTTPException, BackgroundTasks, UploadFile, Path, Depends, File, Form, Query
from sqlalchemy.orm import Session, joinedload

from core import get_db, delete_image
from core.media_settings import save_image
from core.security import get_current_user
from models import User, Review, Product
from .schemas import ReviewsResponse
from .services import update_rating, patch_rating
from ..search.schemas import OrderingParam

router = APIRouter(tags=["Review"])

@router.post('/products/{product_id}/reviews')
async def create_review(background_tasks: BackgroundTasks,
                        product_id: int = Path(...),
                        rating: int = Form(..., ge=1, le=5),
                        text: str | None = Form(None, max_length=500),
                        image: UploadFile | None = File(None, max_length=15 *1024*1024, media_type=['image/png', 'image/jpeg']),
                        author: User = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    ex_review = db.query(Review).filter(Review.author_id == author.id, Review.product_id == product_id).first()
    if ex_review:
        raise HTTPException(status_code=400, detail="You cannot create more than 1 review")

    review = Review(product_id=product_id,
                    author_id=author.id,
                    rating=rating,
                    text=text)
    update_rating(product, rating)
    db.add(review)
    db.flush()

    if image is not None:
        img_path = os.path.join("media", "review", str(review.id))
        ext = image.filename.split('.')[-1]
        path = f"{img_path}.{ext}"
        review.image = path
    

    db.commit()

    if image is not None:
        background_tasks.add_task(save_image, image, path)

    return {"status": "Review created", "review_id": review.id}

@router.get('/products/{product_id}/reviews', response_model=ReviewsResponse)
def get_product_reviews(product_id: int = Path(...),
                        page: int = Query(1, ge=1),
                        size: int = Query(20, le=50),
                        order: OrderingParam = Query(OrderingParam.desc),
                        db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    reviews = (db.query(Review).options(joinedload(Review.author))
               .filter(Review.product_id == product_id)
               .order_by(Review.created_at.desc()
                         if order == OrderingParam.desc
                         else Review.created_at.asc())
               .limit(size+1).offset((page-1)*size)
               .all())
    has_more = True if len(reviews) > size else False

    return {"reviews": reviews[:size], "has_more": has_more}

@router.patch('/reviews/{review_id}')
def edit_review(background_tasks: BackgroundTasks,
                review_id: int = Path(...),
                rating: int | None= Form(None, ge=1, le=5),
                text: str | None = Form(None, max_length=500),
                image: UploadFile | None = File(None, max_length=15 *1024*1024, media_type=['image/png', 'image/jpeg']),
                author: User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    
    review = db.query(Review).options(joinedload(Review.product)).filter(Review.id == review_id, Review.author_id == author.id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    if text is not None: review.text = text
    if image is not None:
        img_path = os.path.join("media", "review", str(review.id))
        ext = image.filename.split('.')[-1]
        path = f"{img_path}.{ext}"
        review.image = path

        background_tasks.add_task(save_image, image, path)

    if rating:
        patch_rating(review.product, review.rating, rating)
        review.rating = rating
    db.commit()

    return {"status": "Review edited"}

@router.delete('/reviews/{review_id}')
def delete_review(review_id: int = Path(...),
                  author: User = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    review = (db.query(Review)
              .options(joinedload(Review.product))
              .filter(Review.id == review_id, Review.author_id == author.id)
              .first()
    )

    if not review:
        raise HTTPException(404, "Review not found")

    product = review.product
    product.reviews_count -= 1
    if product.reviews_count == 0:
        product.rating = 0
    else:
        product.rating = (
            product.rating * (product.reviews_count + 1)
            - review.rating) / product.reviews_count

    db.delete(review)
    db.commit()
    
    return {"status": "Review deleted"}