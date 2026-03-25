from pydantic import BaseModel, EmailStr


class AccountRegisterSchema(BaseModel):
    email: EmailStr
    password: str
    username: str


class AccountLoginSchema(BaseModel):
    email: EmailStr
    password: str


class EmailConfirmation(BaseModel):
    email: str
    code: int
