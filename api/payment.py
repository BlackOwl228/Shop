'''
from fastapi import APIRouter
import stripe
import os

router = APIRouter()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@router.post("/payments/create")
def create_payment():
    intent = stripe.PaymentIntent.create(
        amount=1000,
        currency="usd",
        payment_method_types=["card"],
    )

    return {
        "payment_intent_id": intent.id,
        "client_secret": intent.client_secret,
    }

@router.post("/payments/confirm/{intent_id}")
def confirm_payment(intent_id: str):
    stripe.PaymentIntent.confirm(
        intent_id,
        payment_method="pm_card_visa"
    )
    return {"status": "paid"}
'''