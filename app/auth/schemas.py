from typing import Annotated
from pydantic import BaseModel, EmailStr, Field

UserName = Annotated[str, Field(min_length=5, max_length=100)]
UserEmail = EmailStr
UserPassword = Annotated[str, Field(min_length=8, max_length=128)]

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    
class RefreshResponse(BaseModel):
    access_token: str