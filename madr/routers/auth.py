from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session
from madr.models import User
from madr.database import get_session
from madr.schemas import Token
from madr.security import (
    verify_password, get_current_user,
    create_access_token
)

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@router.post('/token', response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):

    user = session.scalar(
        select(User).where(User.username == form_data.username)
    )

    if not user or not verify_password(
        form_data.password, user.password
    ):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect username or password')

    access_token = create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'Bearer'}


@router.post('/refresh_token', response_model=Token)
async def refresh_access_token(user: User = Depends(get_current_user)):

    new_access_token = create_access_token(data={'sub': user.email})

    return {'access_token': new_access_token, 'token_type': 'Bearer'}
