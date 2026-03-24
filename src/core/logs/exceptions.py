class AppError(Exception):
    status_code = 500
    message = "Internal server error"


class BadRequestError(AppError):
    status_code = 400
    message = "Bad request"


class InvalidRequestFormatError(BadRequestError):
    message = "Invalid request format"


class InvalidOrderStateError(BadRequestError):
    message = "Invalid order state transition"

    def __init__(self, order_id: int, order_status: str):
        self.order_id = order_id
        self.order_status = order_status


class AuthError(AppError):
    status_code = 401
    message = "Auth error"


class InvalidEmailError(AuthError):
    message = "Wrong data, try again"


class InvalidPasswordError(AuthError):
    message = "Wrong data, try again"


class InvalidTokenError(AuthError):
    message = "Invalid token"


class ForbiddenError(AppError):
    status_code = 403
    message = "Forbidden"


class NotYourProductError(ForbiddenError):
    message = "This is not your product"

    def __init__(self, seller_id: int):
        self.seller_id = seller_id


class NotYourOrderError(ForbiddenError):
    message = "This is not your order"

    def __init__(self, order_id: int, user_id: int):
        self.order_id = order_id
        self.user_id = user_id


class NotYourReviewError(ForbiddenError):
    message = "This is not your review"

    def __init__(self, review_id: int, user_id: int):
        self.review_id = review_id
        self.user_id = user_id


class ProductInteractionForbiddenError(ForbiddenError):
    message = "You cannot interact with products now"

    def __init__(self, seller_id: int):
        self.seller_id = seller_id


class NotFoundError(AppError):
    status_code = 404
    message = "Entity not found"


class UserNotFoundError(NotFoundError):
    message = "User not found"

    def __init__(self, user_id: int):
        self.user_id = user_id


class SellerNotFoundError(NotFoundError):
    message = "Seller not found"

    def __init__(self, seller_id: int):
        self.seller_id = seller_id


class ProductNotFoundError(NotFoundError):
    message = "Product not found"

    def __init__(self, product_id: int):
        self.product_id = product_id


class VariantNotFoundError(NotFoundError):
    message = "Variant of product not found"

    def __init__(self, variant_id: int):
        self.variant_id = variant_id


class CategoryNotFoundError(NotFoundError):
    message = "Category not found"

    def __init__(self, category_id: int):
        self.category_id = category_id


class ReviewNotFoundError(NotFoundError):
    message = "Review not found"

    def __init__(self, review_id: int):
        self.review_id = review_id


class OrderNotFoundError(NotFoundError):
    message = "Order not found"

    def __init__(self, order_id: int):
        self.order_id = order_id


class ConflictError(AppError):
    status_code = 409
    message = "Conflict"


class ReviewConflictError(ConflictError):
    message = "You cannot create more than 1 review"

    def __init__(self, author_id: int):
        self.author_id = author_id


class OrderAlreadyPaidError(ConflictError):
    message = "Order already paid"

    def __init__(self, order_id: int):
        self.order_id = order_id


class VariantUnavailableError(ConflictError):
    message = "Variant not available now"

    def __init__(self, variant_id: int):
        self.variant_id = variant_id


class VariantPriceChangedError(ConflictError):
    message = "Variant price has changed"

    def __init__(self, variant_id: int, actual_price):
        self.variant_id = variant_id
        self.actuel_price = actual_price


class VariantOutOfStockError(ConflictError):
    message = "Variant out of stock"

    def __init__(self, variant_id: int, available_stock: int):
        self.variant_id = variant_id
        self.available_stock = available_stock


class VariantAlreadyInCartError(ConflictError):
    message = "Variant already in cart"


class VariantNotInCartError(ConflictError):
    message = "Variant not in cart"


class ProductAlreadyInFavoritesError(ConflictError):
    message = "Product already in favorites"


class ProductNotInFavoritesError(ConflictError):
    message = "Product not in favorites"


class UserAlreadyExistsError(ConflictError):
    message = "User already exists"

    def __init__(self, email: str):
        self.email = email


class SellerAlreadyExistsError(ConflictError):
    message = "Seller or request already exists"

    def __init__(self, user_id: int):
        self.user_id = user_id


class TooManyRequestError(AppError):
    status_code = 429
    message = "Too Many Request"
