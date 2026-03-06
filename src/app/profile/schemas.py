from datetime import datetime

from pydantic import BaseModel, EmailStr


class ProfilePesponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    email_verified: bool
    avatar: str | None
    created_at: datetime
    is_admin: bool
