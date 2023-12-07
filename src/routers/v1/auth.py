from pydantic.dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Body
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel
from jose import jwt
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from models.exceptions.exceptions import UserNotFoundError
from settings import settings
from models.input_schemas.users import CreateInterviewerSchema, CreateRespondentSchema, ChangePasswordSchema
from models.users import InterviewerUser, RespondentUser
from services.db_service import get_db
from services.users import create_interviewer, create_respondent, \
    get_respondent_by_email, get_interviewer_by_email, get_current_user, change_respondent_password, \
    change_interviewer_password

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

user_not_found_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
)

respondent_oauth2_schema = OAuth2PasswordBearer(
    tokenUrl="/auth/respondent-login",
    scheme_name="respondent_oauth2_schema"
)
interviewer_oauth2_schema = OAuth2PasswordBearer(
    tokenUrl="/auth/interviewer-login",
    scheme_name="interviewer_oauth2_schema"
)


class Token(BaseModel):
    access_token: str
    refresh_token: str


async def generate_tokens(user_data) -> Token:
    expire_token_time = datetime.now() + timedelta(minutes=30)
    expire_refresh_token_time = datetime.now() + timedelta(days=365)
    user_data['exp'] = expire_token_time
    access_token = jwt.encode(user_data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    user_data['exp'] = expire_refresh_token_time
    refresh_token = jwt.encode(user_data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return Token(access_token=access_token, refresh_token=refresh_token)


@dataclass
class AdditionalUserDataForm:
    user_type: str


@router.post('/respondent-login', response_model=Token)
async def respondent_login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: Session = Depends(get_db),
):
    """
    Авторизация на основе почты и пароля для респондента
    - **username**: Почта в качестве логина
    - **password**: Пароль
    """
    try:
        user: RespondentUser = await get_respondent_by_email(session=session, email=form_data.username)
    except UserNotFoundError:
        raise user_not_found_exception

    if not user.validate_password(form_data.password):
        raise user_not_found_exception
    user_data = {
        'user_id': user.id,
        'email': user.email,
        'type': 'respondent'
    }
    return await generate_tokens(user_data)


@router.post('/interviewer-login', response_model=Token)
async def interviewer_login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: Session = Depends(get_db),
):
    """
        Авторизация на основе почты и пароля для интервьюера
        - **username**: Почта в качестве логина
        - **password**: Пароль
        """
    try:
        user: InterviewerUser = await get_interviewer_by_email(session=session, email=form_data.username)
    except UserNotFoundError:
        raise user_not_found_exception

    if not user.validate_password(form_data.password):
        raise user_not_found_exception
    user_data = {
        'user_id': user.id,
        'email': user.email,
        'type': 'interviewer'
    }
    return await generate_tokens(user_data)


@router.post('/interviewer-signup', response_model=Token)
async def interviewer_signup(
        payload: CreateInterviewerSchema = Body(),
        session: Session = Depends(get_db),
):
    payload.password = InterviewerUser.hash_password(payload.password)
    user: InterviewerUser = await create_interviewer(session=session, user_data=payload)
    interviewer_user_data = {
        'user_id': user.id,
        'email': user.email,
        'type': 'interviewer'
    }
    return await generate_tokens(interviewer_user_data)


@router.post('/respondent-signup', response_model=Token)
async def respondent_signup(
        payload: CreateRespondentSchema = Body(),
        session: Session = Depends(get_db),
):
    payload.password = RespondentUser.hash_password(payload.password)
    user: RespondentUser = await create_respondent(session=session, user_data=payload)
    respondent_user_data = {
        'user_id': user.id,
        'email': user.email,
        'type': 'respondent'
    }
    return await generate_tokens(respondent_user_data)


@router.put('/change-password-respondent')
async def change_password(
        token: Annotated[str, Depends(respondent_oauth2_schema)],
        payload: ChangePasswordSchema = Body(),
        session: Session = Depends(get_db),
):
    user: RespondentUser = await get_current_user(token=token, session=session)
    if user.validate_password(payload.old_password):
        new_password_hashed = RespondentUser.hash_password(payload.new_password)
        await change_respondent_password(user=user, new_password=new_password_hashed, session=session)
        return JSONResponse(content='Password successful changed')
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect old password')


@router.put('/change-password-interviewer')
async def change_password_interviewer(
        token: Annotated[str, Depends(interviewer_oauth2_schema)],
        payload: ChangePasswordSchema = Body(),
        session: Session = Depends(get_db),
):
    user: RespondentUser = await get_current_user(token=token, session=session)
    if user.validate_password(payload.old_password):
        new_password_hashed = RespondentUser.hash_password(payload.new_password)
        await change_interviewer_password(user=user, new_password=new_password_hashed, session=session)
        return JSONResponse(content='Password successful changed')
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect old password')
