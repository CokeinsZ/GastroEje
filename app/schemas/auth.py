from pydantic import BaseModel

class AuthBase(BaseModel):
    user: str
    password: str