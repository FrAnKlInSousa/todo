from pydantic import BaseModel, EmailStr


class UserPublic(BaseModel):
    username: str
    email: EmailStr
    id: int


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserDB(UserSchema):
    id: int


class UserList(BaseModel):
    users: list[UserPublic]
