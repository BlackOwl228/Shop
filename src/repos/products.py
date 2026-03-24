from sqlalchemy.orm import Session, joinedload

from src.models.products import Product, ProductVariant
from src.rules.product_rules import ProductStatus, available_products


class ProductRepo:
    def __init__(self, db: Session):
        self.db = db

    def commit(self):
        self.db.commit()

    def flush(self):
        self.db.flush()

    def create_product(self, product: Product):
        self.db.add(product)
        self.commit()

    def create_variant(self, variant: ProductVariant):
        self.db.add(variant)
        self.commit()

    def get_product(self, product_id: int):
        return self.db.query(Product).filter(Product.id == product_id).first()

    def get_product_with_variants(self, product_id: int):
        return (
            self.db.query(Product)
            .options(joinedload(Product.variants))
            .filter(Product.id == product_id)
            .first()
        )

    def change_status(self, product: Product, status: ProductStatus):
        product.status = status
        self.db.commit()

    def get_variant(self, variant_id: int):
        return self.db.query(ProductVariant).filter(ProductVariant.id == variant_id).first()

    def get_variant_with_product(self, variant_id):
        return (
            self.db.query(ProductVariant)
            .options(joinedload(ProductVariant.product))
            .filter(ProductVariant.id == variant_id)
            .first()
        )

    def get_available_variants_by_ids(self, variant_ids: list):
        return (
            available_products(self.db.query(ProductVariant)).filter(ProductVariant.id.in_(variant_ids)).all()
        )
