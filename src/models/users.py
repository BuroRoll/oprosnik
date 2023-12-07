import enum
from datetime import datetime, date
from typing import List

import bcrypt
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, LargeBinary, UniqueConstraint, PrimaryKeyConstraint, Enum, Boolean, \
    ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column, backref
from .surveys import Survey

from services.db_service import Base


class FamilyStatus(enum.Enum):
    single = 'не замужем/не женат'
    married = 'замужем/женат'


class IncomeStatus(enum.Enum):
    UP_TO_10000 = "До 10 000 руб."
    FROM_10001_TO_30000 = "10 001 - 30 000 руб."
    FROM_30001_TO_50000 = "30 001 - 50 000 руб."
    FROM_50001_TO_70000 = "50 001 - 70 000 руб."
    FROM_70001_TO_90000 = "70 001 - 90 000 руб."
    FROM_90001_TO_110000 = "90 001 - 110 000 руб."
    OVER_110000 = "110 001+ руб."
    NO_INCOME = "Нет личного дохода."


class EducationStatuses(enum.Enum):
    WITHOUT_EDUCATION = "Без образования"
    INCOMPLETE_SECONDARY = "Неполное среднее"
    SECONDARY = "Среднее"
    SPECIAL_SECONDARY = "Среднее специальное"
    INCOMPLETE_HIGHER = "Неполное высшее"
    HIGHER = "Высшее"
    TWO_OR_MORE_HIGHER = "Два и более высших"
    ACADEMIC_DEGREE = "Ученая степень"


class WorkStatuses(enum.Enum):
    EDUCATION = "Учеба"
    COMMERCIAL_EMPLOYMENT = "Работа по найму в коммерческом секторе"
    OWN_BUSINESS = "Собственный бизнес"
    MILITARY_SERVICE = "Военная служба"
    GOVERNMENT_EMPLOYMENT = "Работа по найму в государственном секторе"
    MATERNITY_LEAVE = "Отпуск по беременности/уходу за ребенком"
    HOUSEHOLD_MANAGEMENT = "Ведение домашнего хозяйства"
    RETIRED = "Пенсионер"
    UNEMPLOYED = "Безработный"
    CLERGY = "Священнослужитель"
    FREELANCE = "Фриланс"
    OTHER = "Другое"


class Languages(enum.Enum):
    ENGLISH = "Английский"
    ITALIAN = "Итальянский"
    SPANISH = "Испанский"
    CHINESE = "Китайский"
    GERMAN = "Немецкий"
    RUSSIAN = "Русский"
    UKRAINIAN = "Украинский"
    FRENCH = "Французский"
    JAPANESE = "Японский"
    OTHER = "Другое"


class RespondentBaseInfo(Base):
    __tablename__ = "respondents_base_info"
    id = Column(Integer, nullable=False, primary_key=True)
    family_status = Column(Enum(FamilyStatus))
    children = Column(Boolean, default=False)
    income = Column(Enum(IncomeStatus))

    PrimaryKeyConstraint("id", name="pk_respondent_info_id")


class RespondentEducation(Base):
    __tablename__ = "respondents_education_info"
    id = Column(Integer, nullable=False, primary_key=True)
    education_status = Column(Enum(EducationStatuses))
    work_status = Column(Enum(WorkStatuses))
    language = Column(Enum(Languages))

    PrimaryKeyConstraint("id", name="pk_respondent_education_info_id")


class RespondentUser(Base):
    __tablename__ = "respondents"
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(LargeBinary, nullable=False)
    gender = Column(String, nullable=False)
    country = Column(String, nullable=False)
    city = Column(String, nullable=False)
    base_info_id = Column(Integer, ForeignKey('respondents_base_info.id'))
    base_info = relationship('RespondentBaseInfo', backref=backref("respondents_base_info", uselist=False))
    education_id = Column(Integer, ForeignKey('respondents_education_info.id'))
    education_info = relationship('RespondentEducation', backref=backref("respondents_education_info", uselist=False))

    UniqueConstraint("email", name="uq_respondent_email")
    PrimaryKeyConstraint("id", name="pk_respondent_id")

    @staticmethod
    def hash_password(password) -> bytes:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def validate_password(self, password) -> bool:
        return bcrypt.checkpw(password.encode(), self.password)


class RespondentBaseData(BaseModel):
    id: int
    family_status: str
    children: bool
    income: str


class RespondentEducationInfo(BaseModel):
    id: int
    education_status: str
    work_status: str
    language: str


class Respondent(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    gender: str
    country: str
    city: str
    base_info: RespondentBaseData
    education_info: RespondentEducationInfo

    class Config:
        from_attributes = True


class InterviewerUser(Base):
    __tablename__ = "interviewers"
    id = Column(Integer, nullable=False, primary_key=True)
    inn = Column(Integer, nullable=False)
    email = Column(String, nullable=False)
    password = Column(LargeBinary, nullable=False)
    organization_name = Column(String, nullable=False)
    surveys = relationship("Survey", backref='intervieweruser')

    UniqueConstraint("email", name="uq_interviewer_email")
    UniqueConstraint("inn", name="uq_interviewer_inn")
    PrimaryKeyConstraint("id", name="pk_interviewer_id")

    @staticmethod
    def hash_password(password) -> bytes:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def validate_password(self, password) -> bool:
        return bcrypt.checkpw(password.encode(), self.password)


class SurveyData(BaseModel):
    id: int
    description: str
    start_date: date
    end_date: date
    status: str


class Interviewer(BaseModel):
    id: int
    inn: int
    email: str
    organization_name: str
    surveys: List[SurveyData]

    class Config:
        from_attributes = True
