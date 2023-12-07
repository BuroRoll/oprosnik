from enum import Enum

from pydantic import BaseModel, Field

from models.users import FamilyStatus, IncomeStatus, Languages, WorkStatuses, EducationStatuses


class Gender(str, Enum):
    man = "Мужчина"
    woman = "Женщина"


class UserType(str, Enum):
    respondent = "respondent"
    interviewer = "interviewer"


class CreateInterviewerSchema(BaseModel):
    inn: int = Field(alias='inn')
    email: str = Field(alias='email')
    password: str = Field(alias='password')


class CreateRespondentSchema(BaseModel):
    name: str = Field(alias='name')
    surname: str = Field(alias='surname')
    email: str = Field(alias='email')
    password: str = Field(alias='password')
    gender: Gender = Field(alias='gender')
    country: str = Field(alias='country')
    city: str = Field(alias='city')


class CreateRespondentBaseInfo(BaseModel):
    family_status: FamilyStatus
    children: bool
    income: IncomeStatus


class CreateRespondentEducationInfo(BaseModel):
    education_status: EducationStatuses
    work_status: WorkStatuses
    language: Languages


class ChangePasswordSchema(BaseModel):
    old_password: str = Field(alias='old_password')
    new_password: str = Field(alias='new_password')
