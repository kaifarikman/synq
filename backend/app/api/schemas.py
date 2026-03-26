from uuid import UUID

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


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str


class ProfileResponse(BaseModel):
    id: int
    user_id: int
    uuid: UUID
    full_name: str | None
    bio: str | None


class UpdateProfileSchema(BaseModel):
    full_name: str | None = None
    bio: str | None = None
