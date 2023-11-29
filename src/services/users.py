from sqlalchemy.orm import Session

from src.models.users import InterviewerUser


# async def get_user(session, phone):
#     return session.query(User).filter(User.phone == phone).one()


# async def create_user(session: Session, user_data):
#     user = User(**user_data.dict())
#     session.add(user)
#     session.commit()
#     return user


async def create_interviewer(session: Session, user_data):
    user = InterviewerUser(**user_data.dict())
    user.organization_name = 'pass'
    session.add(user)
    session.commit()
    return user
