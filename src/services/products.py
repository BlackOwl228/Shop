import os

from sqlalchemy.orm import Session

from src.core.logs.exceptions import (
    NotYourProductError,
    ProductInteractionForbiddenError,
    ProductNotFoundError,
    VariantNotFoundError,
)
from src.models.products import Product, ProductVariant
from src.models.users import Seller
from src.repos.products import ProductRepo
from src.rules.product_rules import ProductStatus
from src.rules.seller_rules import can_interact_product


class ProductService:
    def __init__(self, db: Session):
        self.repo = ProductRepo(db)

    def _check_interact(self, seller):
        if not can_interact_product(seller):
            raise ProductInteractionForbiddenError(seller_id=seller.id)

    def _product_by_id_and_seller_id(self, seller_id: int, product_id: int):
        product = self.repo.get_product(product_id=product_id)
        if not product:
            raise ProductNotFoundError(product_id=product_id)
        if product.seller_id != seller_id:
            raise NotYourProductError(seller_id=seller_id)
        return product

    def _variant_by_id_and_seller_id(self, seller_id: int, variant_id: int):
        variant = self.repo.get_variant_with_product(variant_id=variant_id)
        if not variant:
            raise VariantNotFoundError(variant_id=variant_id)
        if variant.product.seller_id != seller_id:
            raise NotYourProductError(seller_id=seller_id)
        return variant

    def _create_image_path(self, product_id: int, variant_id: int, image):
        img_path = os.path.join("media", "product", str(product_id), str(variant_id))
        ext = image.filename.split(".")[-1]
        path = f"{img_path}.{ext}"
        return path

    def create_product(self, seller: Seller, name: str, description: str):
        self._check_interact(seller=seller)
        product = Product(name=name, description=description, seller_id=seller.id)
        self.repo.create_product(product)

        return product

    def get_product(self, product_id: int):
        product = self.repo.get_product(product_id=product_id)
        if not product:
            raise ProductNotFoundError(product_id=product_id)

        return product

    def get_full_product_by_id(self, product_id: int):
        product = self.repo.get_product_with_variants(product_id=product_id)
        if not product:
            raise ProductNotFoundError(product_id=product_id)

        return product

    def change_product(self, seller: Seller, product_id: int, name: str, description: str):
        self._check_interact(seller=seller)
        product = self._product_by_id_and_seller_id(product_id=product_id, seller_id=seller.id)
        if name:
            product.name = name
        if description:
            product.description = description
        self.repo.commit()

    def delete_product(self, seller: Seller, product_id: int):
        self._check_interact(seller=seller)
        product = self._product_by_id_and_seller_id(product_id=product_id, seller_id=seller.id)
        product.status = ProductStatus.DELETED
        self.repo.commit()

    def create_variant(self, seller: Seller, name: str, price: float, product_id: int, stock: int, image):
        self._check_interact(seller=seller)
        variant = ProductVariant(name=name, price=price, product_id=product_id, stock=stock)
        self.repo.create_variant(variant=variant)
        if image is not None:
            self.repo.flush()
            variant.image = self._create_image_path(product_id=product_id, variant_id=variant.id, image=image)
        self.repo.commit()

        return variant

    def change_variant(
        self, seller: Seller, product_id: int, variant_id: int, name: str, price: float, stock: int, image
    ):
        self._check_interact(seller=seller)
        variant = self._variant_by_id_and_seller_id(variant_id=variant_id, seller_id=seller.id)

        if name:
            variant.name = name
        if price:
            variant.price = price
        if stock:
            variant.stock = stock
        if image:
            variant.image = self._create_image_path(
                variant=variant, product_id=product_id, variant_id=variant.id, image=image
            )
        self.repo.commit()
        return variant

    def change_stock(self, seller: Seller, variant_id: int, stock_delta: int):
        self._check_interact(seller=seller)
        variant = self._variant_by_id_and_seller_id(variant_id=variant_id, seller_id=seller.id)
        variant.stock = max(0, variant.stock + stock_delta)
        self.repo.commit()
