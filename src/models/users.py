from enum import Enum

import bcrypt
from sqlalchemy import Column, Integer, String, LargeBinary, UniqueConstraint, PrimaryKeyConstraint

from src.services.db_service import Base


class Gender(str, Enum):
    man = "Мужчина"
    woman = "Женщина"


# class User(Base):
#     @staticmethod
#     def hash_password(password) -> bytes:
#         return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
#
#     def validate_password(self, password) -> bool:
#         """Confirms password validity"""
#         return bcrypt.checkpw(password.encode(), self.password)
#
#     def generate_token(self):
#         pass


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

    UniqueConstraint("email", name="uq_respondent_email")
    PrimaryKeyConstraint("id", name="pk_respondent_id")

    @staticmethod
    def hash_password(password) -> bytes:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


class InterviewerUser(Base):
    __tablename__ = "interviewers"
    id = Column(Integer, nullable=False, primary_key=True)
    inn = Column(Integer, nullable=False)
    email = Column(String, nullable=False)
    password = Column(LargeBinary, nullable=False)
    organization_name = Column(String, nullable=False)

    UniqueConstraint("email", name="uq_interviewer_email")
    UniqueConstraint("inn", name="uq_interviewer_inn")
    PrimaryKeyConstraint("id", name="pk_interviewer_id")

    @staticmethod
    def hash_password(password) -> bytes:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
