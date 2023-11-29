from pydantic import BaseModel, Field


class UserBaseSchema(BaseModel):
    phone: str
    name: str
    surname: str


class CreateUserSchema(UserBaseSchema):
    password: str = Field(alias="password")


class CreateInterviewerSchema(BaseModel):
    inn: int = Field(alias='inn')
    email: str = Field(alias='email')
    password: str = Field(alias='password')
