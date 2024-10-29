from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from http import HTTPStatus

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session
from pwdlib import PasswordHash
from jwt import decode, encode
from jwt.exceptions import PyJWTError, ExpiredSignatureError

from madr.database import get_session
from madr.models import User
from madr.settings import Settings

pwd_context = PasswordHash.recommended()
oauth2_schema = OAuth2PasswordBearer(tokenUrl='auth/token')
settings = Settings()


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({'exp': expire})

    encoded_jwt = encode(to_encode, settings.SECRET_KEY,
                         algorithm=settings.ALGORITHM)

    return encoded_jwt


def get_current_user(
        session: Session = Depends(get_session),
        token: str = Depends(oauth2_schema)
):

    credentials_exeption = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )

    try:
        payload = decode(token, settings.SECRET_KEY,
                         algorithms=settings.ALGORITHM)
        username = payload.get('sub')

        if not username:
            raise credentials_exeption

    except ExpiredSignatureError:
        raise credentials_exeption
    except PyJWTError:
        raise credentials_exeption

    user = session.scalar(
        select(User).where(User.email == username)
    )

    if not user:
        raise credentials_exeption

    return user
