from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from typing import Annotated, Union, List
from fastapi.params import Body, Query

from sqlalchemy.orm import Session
from starlette import status

from models.input_schemas.surveys import CreateSurveyScheme
from models.response_schemas.surveys import SurveyResponseModel
from models.surveys import SurveyStatus
from services.db_service import get_db
from services.surveys import save_survey, get_survey, get_surveys
from services.users import get_current_user

from models.users import InterviewerUser

interviewer_oauth2_schema = OAuth2PasswordBearer(
    tokenUrl="/auth/interviewer-login",
    scheme_name="interviewer_oauth2_schema"
)

router = APIRouter(
    prefix="/survey",
    tags=["surveys"],
)


@router.post('/', status_code=201, response_model=SurveyResponseModel)
async def create_survey(
        token: Annotated[str, Depends(interviewer_oauth2_schema)],
        survey_info: CreateSurveyScheme = Body(),
        session: Session = Depends(get_db),
):
    user: InterviewerUser = await get_current_user(token=token, session=session)
    try:
        survey = await save_survey(interviewer=user, survey_data=survey_info, session=session)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create survey",
        )
    return survey


@router.get('/my', response_model=Union[SurveyResponseModel, list[SurveyResponseModel]])
async def get_survey_(
        token: Annotated[str, Depends(interviewer_oauth2_schema)],
        survey_id: Annotated[
            int | None,
            Query(
                title="Survey Id",
                description="id опроса, если пустое, то вернет все опросы текущего пользователя",
            ),
        ] = None,
        session: Session = Depends(get_db),
):
    user: InterviewerUser = await get_current_user(token=token, session=session)
    if survey_id:
        survey = await get_survey(survey_id=survey_id, user_id=user.id, session=session)
        return survey
    else:
        surveys = await get_surveys(user_id=user.id, session=session)
        return surveys


@router.put('/status')
async def set_new_status(
        new_status: SurveyStatus,
        token: Annotated[str, Depends(interviewer_oauth2_schema)],
        survey_id: Annotated[
            int | None,
            Query(
                title="Survey Id",
                description="id опроса, для которого необходимо сменить статус",
            ),
        ],

):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)
