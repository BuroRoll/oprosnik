from datetime import date
from typing import List

from pydantic import BaseModel


class QuestionsResponseModel(BaseModel):
    question_text: str
    question_type: str
    question_answers: str
    id: int
    question_number: int
    survey_id: int


class SurveyResponseModel(BaseModel):
    id: int
    interviewer_id: int
    description: str
    start_date: date
    end_date: date
    status: str
    questions: List[QuestionsResponseModel]
