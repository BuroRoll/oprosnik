from sqlalchemy.orm import Session, contains_eager, subqueryload

from models.input_schemas.surveys import CreateSurveyScheme
from models.surveys import Survey, Question
from models.users import InterviewerUser


async def save_survey(
        interviewer: InterviewerUser,
        survey_data: CreateSurveyScheme,
        session: Session
) -> Survey:
    survey_data = survey_data.model_dump()
    questions = survey_data.pop("questions")
    survey = Survey(**survey_data)
    session.add(survey)
    session.commit()
    session.refresh(survey)
    for question_data in questions:
        question_data['question_answers'] = str(question_data['question_answers'])
        question = Question(**question_data)
        session.add(question)
        session.commit()
        session.refresh(question)
        survey.questions.append(question)
        print(survey)
    interviewer.surveys.append(survey)
    session.commit()
    session.refresh(survey)
    return survey


async def get_survey(survey_id: int, user_id: int, session: Session):
    survey = session.query(Survey). \
        options(subqueryload(Survey.questions)). \
        filter(Survey.id == survey_id). \
        first()
    if survey.interviewer_id != user_id:
        raise Exception('Not your survey')
    return survey


async def get_surveys(user_id: int, session: Session):
    surveys = session.query(Survey).options(subqueryload(Survey.questions)).filter(Survey.interviewer_id == user_id).all()
    return surveys
