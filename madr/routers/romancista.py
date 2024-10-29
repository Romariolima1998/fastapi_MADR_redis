from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr.models import User, Romancista
from madr.database import get_session
from madr.security import get_current_user
from madr.schemas import (
    Message, RomancistaSchema, RomancistaPublic, RomancistaPublicList
)
from madr.utils import string_handling


router = APIRouter(
    prefix='/romancista',
    tags=['romancista']
)
GetSession = Annotated[Session, Depends(get_session)]
GetCurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_romancista(
    dados: RomancistaSchema, session: GetSession, current_user: GetCurrentUser
) -> RomancistaPublic:

    romancista = session.scalar(
        select(Romancista).where(Romancista.nome == dados.nome)
    )

    if romancista:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='romancista já consta no MADR'
        )

    romancista = Romancista(nome=string_handling(dados.nome))

    session.add(romancista)
    session.commit()
    session.refresh(romancista)

    return romancista


@router.get('/{id}')
async def read_romanticista_id(
        id: int, session: GetSession) -> RomancistaPublic:

    romancista = session.scalar(
        select(Romancista).where(Romancista.id == id)
    )

    if not romancista:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Romancista não consta no MADR"
        )

    return romancista


@router.get('/')
async def read_romanticista_query(
        nome: str, session: GetSession) -> RomancistaPublicList:

    romancistas = session.scalars(
        select(Romancista).filter(Romancista.nome.contains(nome))
    )

    return {'romancistas': romancistas}


@router.patch('/{id}')
async def update_romancista(
    id: int, dados: RomancistaSchema, session: GetSession,
    current_user: GetCurrentUser
) -> RomancistaPublic:

    romancista = session.scalar(
        select(Romancista).where(Romancista.id == id)
    )

    if not romancista:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Romancista não consta no MADR'
        )

    if dados.nome:
        romancista.nome = string_handling(dados.nome)

    session.commit()
    session.refresh(romancista)

    return romancista


@router.delete('/{id}')
async def delete_romancista(
    id: int, session: GetSession, current_user: GetCurrentUser
) -> Message:

    romancista = session.scalar(
        select(Romancista).where(Romancista.id == id)
    )

    if not romancista:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Romancista não consta no MADR'
        )

    session.delete(romancista)
    session.commit()

    return {'message': 'Romancista deletada no MADR'}
