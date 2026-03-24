from sqlalchemy.orm import Session

from src.models.orders import Order


class OrderRepo:
    def __init__(self, db: Session):
        self.db = db

    def commit(self):
        self.db.commit()

    def create(self, order: Order):
        self.db.add(order)

    def get(self, order_id: int):
        return self.db.query(Order).filter(Order.id == order_id).first()
