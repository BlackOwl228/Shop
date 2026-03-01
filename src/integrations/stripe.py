import stripe
from fastapi import HTTPException
from models.orders import Order

def create_payment(amount: int):
    intent = stripe.PaymentIntent.create(
        amount=amount,
        currency="rub",
        payment_method_types=["card"],  # для тестов
    )
    return intent.id, intent.client_secret

def confirm_payment(order: Order):
    # подтверждаем тестовой картой pm_card_visa
    intent = stripe.PaymentIntent.confirm(
        order.payment_intent,
        payment_method="pm_card_visa"
    )

    if intent.status == "succeeded":
        order.status = "paid"
    else:
        raise HTTPException(status_code=400, detail=f"Payment failed: {intent.status}")