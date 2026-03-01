from fastapi import APIRouter, Request
from ..config import templates

router = APIRouter(tags=["FOR WEBSITE"])

@router.get("/front/checkout")
def checkout_page(request: Request):
    return templates.TemplateResponse("checkout.html", {"request": request})