from pydantic import BaseModel, EmailStr


class AccountSchema(BaseModel):
    email: EmailStr
    password: str
    username: str


class EmailConfirmation(BaseModel):
    email: str
    code: int
