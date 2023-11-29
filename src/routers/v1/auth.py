from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Body
from starlette import status
from sqlalchemy.orm import Session

from src.models.input_schemas.users import CreateUserSchema, CreateInterviewerSchema
from src.models.users import InterviewerUser
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from fastapi_jwt_auth import AuthJWT
from src.services.db_service import get_db
# from src.services.users import get_user, create_user, create_interviewer
from src.services.users import create_interviewer

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


# @router.post('/login')
# async def login(payload: OAuth2PasswordRequestForm = Depends(),
#                 session: Session = Depends(get_db),
#                 # Authorize: AuthJWT = Depends()
#                 ):
#     try:
#         user: User = await get_user(
#             session=session, phone=payload.username
#         )
#     except Exception as e:
#         print(e)
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid user credentials"
#         )
#
#     is_validated: bool = user.validate_password(payload.password)
#     if not is_validated:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid user credentials"
#         )
#     # access_token = Authorize.create_access_token(subject=user.username)
#     # refresh_token = Authorize.create_refresh_token(subject=user.username)
#     return user.generate_token()


# @router.post('/signup')
# async def signup(
#         payload: CreateUserSchema = Body(),
#         session: Session = Depends(get_db)
# ):
#     """Processes request to register user account."""
#     payload.password = User.hash_password(payload.password)
#     return await create_user(session=session, user_data=payload)


@router.post('/interviewer-login')
async def interviewer_login(
        payload: OAuth2PasswordRequestForm = Depends(),
        session: Session = Depends(get_db),
        # authorize: AuthJWT = Depends()
):
    pass


@router.post('/respondent-login')
async def respondent_login(
        payload: OAuth2PasswordRequestForm = Depends(),
        session: Session = Depends(get_db),
        # authorize: AuthJWT = Depends()
):
    pass


@router.post('/interviewer-signup')
async def signup(
        payload: CreateInterviewerSchema = Body(),
        session: Session = Depends(get_db)
):
    """Processes request to register user account."""
    payload.password = InterviewerUser.hash_password(payload.password)
    return await create_interviewer(session=session, user_data=payload)
