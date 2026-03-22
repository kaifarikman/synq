from pydantic import BaseModel


class AccountSchema(BaseModel):
    email: str
    password: str
