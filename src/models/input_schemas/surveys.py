from datetime import date
from typing import List, Union

from pydantic import BaseModel, Field

from models.surveys import QuestionType


class QuestionAnswersSchema(BaseModel):
    answers: List[str] = Field(alias='answers')


class QuestionsSchema(BaseModel):
    question_text: str = Field(alias='question_text')
    question_number: int = Field(alias='question_number')
    question_type: QuestionType = Field(alias='question_type')
    question_answers: QuestionAnswersSchema = Field(alias='question_answers')


class CreateSurveyScheme(BaseModel):
    description: str = Field(alias='description')
    start_date: date = Field(alias='start_date')
    end_date: date = Field(alias='end_date')
    questions: List[QuestionsSchema] = Field(alias='questions')
