from datetime import UTC, datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from models.tokens import EmailToken


class EmailService:
    def __init__(self, db: Session):
        self.db = db

    def verify_email_by_token(self, token):
        token = (
            self.db.query(EmailToken)
            .options(joinedload(EmailToken.user))
            .filter(EmailToken.id == token, EmailToken.expires_at >= datetime.now(UTC))
            .first()
        )
        if not token:
            raise HTTPException(status_code=404, detail="Token not found")

        token.user.email_verified = True
        self.db.delete(token)
        self.db.commit()
