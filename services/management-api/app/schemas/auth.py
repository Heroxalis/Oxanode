from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    username: str = Field(min_length=3, max_length=64)
    password: str = Field(min_length=1, max_length=256)

class LoginResponse(BaseModel):
    authenticated: bool
    message: str

class AdminResponse(BaseModel):
    username: str
    authenticated: bool