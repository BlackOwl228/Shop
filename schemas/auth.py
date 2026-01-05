from pydantic import BaseModel, EmailStr, Field

class UserName(BaseModel):
    name: str = Field(min_length=5, max_length=100, example="User123")

class UserEmail(BaseModel):
    email: EmailStr

class UserPassword(BaseModel):
    password: str = Field(min_length=6, max_length=128)

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = Field(..., example="bearer")
    
class RefreshResponse(BaseModel):
    access_token: str