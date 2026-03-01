from fastapi import APIRouter, Depends, HTTPException, Request, Path
from sqlalchemy.orm import Session
from sqlalchemy import func

from src.core.db import get_db
from src.models.products import Product
from ..config import templates

router = APIRouter(prefix='/front', tags=["FOR WEBSITE"])

@router.get("/home")
def front_home(
    request: Request,
    db: Session = Depends(get_db),
):
    products = (
        db.query(Product)
        .order_by(func.random())
        .limit(20)
        .all()
    )

    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "products": products,
        },
    )

@router.get("/products/{product_id}")
def product_page(
    product_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    product = db.query(Product).get(product_id)

    if not product:
        raise HTTPException(status_code=404)

    return templates.TemplateResponse(
        "product.html",
        {
            "request": request,
            "product": product
        }
    )