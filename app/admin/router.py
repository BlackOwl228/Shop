from fastapi import APIRouter, HTTPException, Depends, Path, Form
from sqlalchemy.orm import Session

from core import get_db
from core.security import get_current_admin
from models import User, Product, Order, Seller, Review, Category
from rules import ProductStatus, SellerStatus, OrderStatus

router = APIRouter(prefix='/admin', tags=["Admin"])

@router.delete('/products/{product_id}/block')
def block_products(product_id: int = Path(...),
                   admin: User = Depends(get_current_admin),
                   db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.status == ProductStatus.BLOCKED:
        return {"status": "Already blocked"}
    
    product.status = ProductStatus.BLOCKED
    db.commit()

@router.patch('/products/{product_id}/unblock')
def unblock_products(product_id: int = Path(...),
                     admin: User = Depends(get_current_admin),
                     db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.status == ProductStatus.ACTIVE:
        return {"status": "Already unblocked"}

    product.status = ProductStatus.ACTIVE
    db.commit()


@router.post('/sellers/{seller_id}')
def approve_seller_request(seller_id: int = Path(...),
                           admin: User = Depends(get_current_admin),
                           db: Session = Depends(get_db)):
    request = db.query(Seller).filter(Seller.id == seller_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    if request.status == SellerStatus.ACTIVE:
        return {"status": "Already approved"}
    
    request.status = SellerStatus.ACTIVE
    db.commit()

    return {"status": f"Seller {seller_id} was approved"}

@router.delete('/sellers/{seller_id}')
def suspend_seller(seller_id: int = Path(...),
                   admin: User = Depends(get_current_admin),
                   db: Session = Depends(get_db)):
    seller = db.query(Seller).filter(Seller.id == seller_id).first()
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    if seller.status == SellerStatus.SUSPENDED:
        return {"status": "Already suspended"}
    
    seller.status = SellerStatus.SUSPENDED
    db.commit()

    return {"status": f"Seller {seller_id} was suspended"}


@router.patch('/orders/{order_id}/complete')
def complete_order(order_id: int = Path(...),
                   admin: User = Depends(get_current_admin),
                   db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status != OrderStatus.PAID:
        return {"status": "Order not paid yet, you cannot complete it"}
    
    order.status = OrderStatus.COMPLETED
    db.commit()

@router.patch('/orders/{order_id}/cancel')
def cancel_order(order_id: int = Path(...),
                 admin: User = Depends(get_current_admin),
                 db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status == OrderStatus.PAID:
        return {"status": "Order already paid you cannot cancel it"}
    
    order.status = OrderStatus.CANCELLED
    db.commit()


@router.delete('/reviews/{review_id}')
def delete_review(review_id: int = Path(...),
                  admin: User = Depends(get_current_admin),
                  db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    db.delete(review)
    db.commit()

@router.post('/categories')
def make_category(name: str,
                  admin: User = Depends(get_current_admin),
                  db: Session = Depends(get_db)):
    db.add(Category(name=name))
    db.commit()
    return{"status": "created"}

@router.post('/products/{product_id}/categories/{category_id}')
def add_product_to_category(product_id: int = Path(...),
                            category_id: int = Path(...),
                            admin: User = Depends(get_current_admin),
                            db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    product.category=category
    db.commit()