from sqlalchemy.orm import Session


class AdminRepo:
    def __init__(self, db: Session):
        self.db = db
