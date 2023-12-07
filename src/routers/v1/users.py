from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from typing import Annotated, Union
from fastapi.params import Body

from sqlalchemy.orm import Session
from starlette import status

from models.input_schemas.users import CreateRespondentBaseInfo, CreateRespondentEducationInfo
from services.db_service import get_db
from services.users import create_respondent_base_info, \
    create_respondent_education_info, get_current_user
from models.users import RespondentUser, Interviewer, Respondent

respondent_oauth2_schema = OAuth2PasswordBearer(
    tokenUrl="/auth/respondent-login",
    scheme_name="respondent_oauth2_schema"
)
interviewer_oauth2_schema = OAuth2PasswordBearer(
    tokenUrl="/auth/interviewer-login",
    scheme_name="interviewer_oauth2_schema"
)

router = APIRouter(
    prefix="/user",
    tags=["users"],
)


@router.get('/respondent-info', response_model=Respondent)
async def get_respondent_info(
        token: Annotated[str, Depends(respondent_oauth2_schema)],
        session: Session = Depends(get_db),
):
    return await get_current_user(token=token, session=session)


@router.get('/interviewer-info', response_model=Interviewer)
async def get_interviewer_info(
        token: Annotated[str, Depends(interviewer_oauth2_schema)],
        session: Session = Depends(get_db),
):
    return await get_current_user(token=token, session=session)


@router.put('/respondent/base-info', response_model=Respondent)
async def append_respondent_base_info(
        token: Annotated[str, Depends(respondent_oauth2_schema)],
        respondent_base_info: CreateRespondentBaseInfo = Body(),
        session: Session = Depends(get_db),
):
    user: RespondentUser = await get_current_user(token=token, session=session)
    try:
        user = await create_respondent_base_info(
            user=user,
            respondent_base_info=respondent_base_info,
            session=session
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create base info",
        )
    return user


@router.put('/respondent/education-info', response_model=Respondent)
async def append_respondent_education_info(
        token: Annotated[str, Depends(respondent_oauth2_schema)],
        respondent_education_info: CreateRespondentEducationInfo = Body(),
        session: Session = Depends(get_db),
):
    user: RespondentUser = await get_current_user(token=token, session=session)
    try:
        user = await create_respondent_education_info(
            user=user,
            respondent_education_info=respondent_education_info,
            session=session
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create education info",
        )
    return user
