import os

from sqlalchemy.orm import Session

from src.core.logs.exceptions import (
    CategoryNotFoundError,
    NotYourProductError,
    ProductInteractionForbiddenError,
    ProductNotFoundError,
    VariantNotFoundError,
)
from src.models.collections import Category
from src.models.products import Product, ProductVariant
from src.models.users import Seller
from src.rules.product_rules import ProductStatus
from src.rules.seller_rules import can_interact_product


class ProductService:
    def __init__(self, db: Session, seller: Seller):
        self.db = db
        self.seller = seller

    def _check_interact(self):
        if not can_interact_product(self.seller):
            raise ProductInteractionForbiddenError(seller_id=self.seller.id)

    def _product_by_id_and_seller_id(self, product_id):
        product = (
            self.db.query(Product)
            .filter(Product.id == product_id, Product.seller_id == self.seller.id)
            .first()
        )
        if not product:
            raise ProductNotFoundError(product_id=product_id)
        return product

    def _variant_by_ids(self, product_id, variant_id):
        variant = (
            self.db.query(ProductVariant)
            .join(Product)
            .filter(
                ProductVariant.product_id == product_id,
                ProductVariant.id == variant_id,
                Product.seller_id == self.seller.id,
            )
            .first()
        )
        if not variant:
            raise VariantNotFoundError(variant_id=variant_id)
        return variant

    def _create_image_path(self, variant, product_id, variant_id, image):
        img_path = os.path.join("media", "product", str(product_id), str(variant_id))
        ext = image.filename.split(".")[-1]
        path = f"{img_path}.{ext}"
        variant.image = path
        return path

    def create_product(self, name, description):
        self._check_interact()
        product = Product(name=name, description=description, seller_id=self.seller.id)
        self.db.add(product)
        self.db.commit()

        return product

    def change_product(self, product_id, name, description):
        self._check_interact()
        product = self._product_by_id_and_seller_id(product_id)
        if name:
            product.name = name
        if description:
            product.description = description
        self.db.commit()

    def delete_product(self, product_id):
        self._check_interact()
        product = self._product_by_id_and_seller_id(product_id)
        product.status = ProductStatus.DELETED
        self.db.commit()

    def create_variant(self, name, price, product_id, stock, image):
        self._check_interact()
        variant = ProductVariant(name=name, price=price, product_id=product_id, stock=stock)
        self.db.add(variant)
        if image is not None:
            self.db.flush()
            variant.image = self._create_image_path(
                variant=variant, product_id=product_id, variant_id=variant.id, image=image
            )
        self.db.commit()

        return variant

    def change_variant(self, product_id, variant_id, name, price, stock, image):
        self._check_interact()
        variant = self._variant_by_ids(product_id=product_id, variant_id=variant_id)

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
        self.db.commit()
        return variant

    def change_stock(self, product_id, variant_id, stock_delta):
        self._check_interact()
        variant = self._variant_by_ids(product_id=product_id, variant_id=variant_id)
        variant.stock = max(0, variant.stock + stock_delta)
        self.db.commit()

    def change_product_category(self, product_id, category_id):
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise ProductNotFoundError(product_id=product_id)
        if product.seller_id != self.seller.id:
            raise NotYourProductError(seller_id=self.seller.id)

        category = self.db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise CategoryNotFoundError(category_id=category_id)

        product.category = category
        self.db.commit()
