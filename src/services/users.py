from typing import Type

from fastapi import HTTPException
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from models.exceptions.exceptions import UserNotFoundError
from models.input_schemas.users import CreateRespondentBaseInfo, CreateRespondentEducationInfo, CreateRespondentSchema, \
    CreateInterviewerSchema
from models.users import InterviewerUser, RespondentUser, RespondentBaseInfo, RespondentEducation
from settings import settings


async def create_interviewer(
        session: Session,
        user_data: CreateInterviewerSchema
) -> InterviewerUser:
    user = InterviewerUser(**user_data.dict())
    # TODO сделать получение названия по ИНН
    user.organization_name = 'pass'
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


async def get_interviewer_by_email(
        session: Session,
        email: str
) -> InterviewerUser:
    interviewer = session.query(InterviewerUser).filter(InterviewerUser.email == email).first()
    if interviewer is None:
        raise UserNotFoundError
    return interviewer


async def get_interviewer_by_id(
        session: Session,
        user_id: int
) -> InterviewerUser:
    interviewer = session.query(InterviewerUser).filter(InterviewerUser.id == user_id).first()
    if interviewer is None:
        raise UserNotFoundError
    return interviewer


async def create_respondent(
        session: Session,
        user_data: CreateRespondentSchema
) -> RespondentUser:
    user = RespondentUser(**user_data.dict())
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


async def get_respondent_by_email(
        session: Session,
        email: str
) -> RespondentUser:
    respondent = session.query(RespondentUser).filter(RespondentUser.email == email).first()
    if respondent is None:
        raise UserNotFoundError
    return respondent


async def get_respondent_by_id(
        session: Session,
        user_id: int
) -> RespondentUser:
    respondent = session.query(RespondentUser).filter(RespondentUser.id == user_id).first()
    if respondent is None:
        raise UserNotFoundError
    return respondent


async def create_respondent_base_info(
        user: RespondentUser,
        respondent_base_info: CreateRespondentBaseInfo,
        session: Session
) -> RespondentUser:
    if user.base_info is None:
        base_info: RespondentBaseInfo = RespondentBaseInfo(**respondent_base_info.dict())
        session.add(base_info)
        session.commit()
        session.refresh(base_info)
        user.base_info = base_info
        session.add(user)
        session.commit()
        session.refresh(user)
    else:
        info_id = user.base_info_id
        session.query(RespondentBaseInfo).filter(RespondentBaseInfo.id == info_id).update(
            respondent_base_info.dict())
        session.commit()
        session.refresh(user)
    return user


async def create_respondent_education_info(
        user: RespondentUser,
        respondent_education_info: CreateRespondentEducationInfo,
        session: Session
):
    if user.education_info is None:
        education_info: RespondentEducation = RespondentEducation(**respondent_education_info.dict())
        session.add(education_info)
        session.commit()
        session.refresh(education_info)
        user.education_info = education_info
        session.add(user)
        session.commit()
        session.refresh(user)
    else:
        education_id: int = user.education_id
        session.query(RespondentEducation).filter(RespondentEducation.id == education_id).update(
            respondent_education_info.dict())
        session.commit()
        session.refresh(user)

    return user


async def get_current_user(
        token: str,
        session: Session
) -> InterviewerUser | RespondentUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        user_id: int = payload.get('user_id')
        user_type: str = payload.get('type')
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    match user_type:
        case 'respondent':
            user: RespondentUser = await get_respondent_by_id(session, user_id=user_id)
        case 'interviewer':
            user: InterviewerUser = await get_interviewer_by_id(session, user_id=user_id)
        case _:
            raise credentials_exception
    if user is None:
        raise credentials_exception
    return user


async def change_respondent_password(
        user: RespondentUser,
        new_password: bytes,
        session: Session
):
    user.password = new_password
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


async def change_interviewer_password(
        user: InterviewerUser,
        new_password: bytes,
        session: Session
):
    user.password = new_password
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
