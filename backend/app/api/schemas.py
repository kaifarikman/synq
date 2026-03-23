from pydantic import BaseModel, EmailStr


class AccountSchema(BaseModel):
    email: EmailStr
    password: str
