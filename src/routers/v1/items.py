from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(oauth2_scheme)],
    responses={404: {"description": "Not found"}},
)

fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}


@router.get("/")
async def read_items():
    return fake_items_db
