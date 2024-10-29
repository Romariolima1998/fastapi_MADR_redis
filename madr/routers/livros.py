from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr.models import User, Romancista, Livro
from madr.database import get_session
from madr.security import get_current_user
from madr.schemas import (
    Message, LivroSchema, LivroPublic, ListLivroPublic, LivroUpdate
)
from madr.utils import string_handling


router = APIRouter(
    prefix='/livros',
    tags=['livros']
)
GetSession = Annotated[Session, Depends(get_session)]
GetCurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_livro(
    dados: LivroSchema, session: GetSession, current_user: GetCurrentUser
) -> LivroPublic:

    romancista_id = session.scalar(
        select(Romancista).where(Romancista.id == dados.id_romancista)
    )

    if not romancista_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='romancista_id nao coincide com nenhum romancista'
        )

    livro = session.scalar(
        select(Livro).where(Livro.titulo == dados.titulo)
    )

    if livro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='livro já consta no MADR'
        )

    livro = Livro(ano=dados.ano, titulo=string_handling(dados.titulo),
                  id_romancista=dados.id_romancista)

    session.add(livro)
    session.commit()
    session.refresh(livro)

    return livro


@router.get('/{id}')
async def read_livro_id(id: int, session: GetSession) -> LivroPublic:

    livro = session.scalar(
        select(Livro).where(Livro.id == id)
    )

    if not livro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não consta no MADR"
        )

    return livro


@router.get('/')
async def read_livro_query(nome: str, session: GetSession) -> ListLivroPublic:

    livros = session.scalars(
        select(Livro).filter(Livro.titulo.contains(nome))
    )

    return {'livros': livros}


@router.patch('/{id}', response_model=LivroPublic)
async def update_livro(
        id: int, dados: LivroUpdate, session: GetSession,
        current_user: GetCurrentUser):

    livro = session.scalar(
        select(Livro).where(Livro.id == id)
    )

    if not livro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Livro não consta no MADR'
        )
    if dados.titulo:
        dados.titulo = string_handling(dados.titulo)

    for key, value in dados.model_dump(exclude_unset=True).items():
        setattr(livro, key, value)

    session.commit()
    session.refresh(livro)

    return livro


@router.delete('/{id}')
async def delete_livro(
        id: int, session: GetSession, current_user: GetCurrentUser
) -> Message:

    livro = session.scalar(
        select(Livro).where(Livro.id == id)
    )

    if not livro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Livro não consta no MADR'
        )

    session.delete(livro)
    session.commit()

    return {'message': "Livro deletado no MADR"}
