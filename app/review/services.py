from models import Product
def update_rating(product: Product, new_rating: int):
    total = product.rating * product.reviews_count
    total += new_rating

    product.reviews_count += 1
    product.rating = total / product.reviews_count

def patch_rating(product: Product, old_rating: int, new_rating: int):
    product.rating = (
    product.rating * product.reviews_count
    - old_rating
    + new_rating) / product.reviews_count