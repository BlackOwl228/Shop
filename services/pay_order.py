import stripe

def create_payment(amount: int):
    intent = stripe.PaymentIntent.create(
        amount=amount,
        currency="rub",
        payment_method_types=["card"],  # для тестов
    )
    return intent.id