import datetime
import enum

from sqlalchemy import Column, Integer, Text, Date, ForeignKey, Enum, PrimaryKeyConstraint
from sqlalchemy.orm import relationship, backref

from services.db_service import Base


class SurveyStatus(enum.Enum):
    active = 'Активный'
    inactive = 'Неактивный'


class QuestionType(enum.Enum):
    single_chose = 'Одиночный выбор'
    multiple_chose = 'Множественный выбор'
    text = 'Открытый ответ'


class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, nullable=False, primary_key=True)
    question_text = Column(Text, nullable=False)
    question_number = Column(Integer, nullable=False)
    question_type = Column(Enum(QuestionType))
    # Не придумал пока ничего лучше, чем сохранить вариант ответа в БД просто в JSON
    question_answers = Column(Text, nullable=False)
    survey_id = Column(Integer, ForeignKey('surveys.id'))


class Survey(Base):
    __tablename__ = "surveys"
    id = Column(Integer, nullable=False, primary_key=True)
    description = Column(Text, nullable=True)
    start_date = Column(Date, default=datetime.datetime.utcnow, nullable=False)
    end_date = Column(Date, nullable=False)
    interviewer_id = Column(Integer, ForeignKey('interviewers.id'))
    status = Column(Enum(SurveyStatus), default='inactive')
    questions = relationship("Question", backref='survey')

    PrimaryKeyConstraint("id", name="pk_survey_id")
