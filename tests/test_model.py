from datetime import datetime
from madr.models import User, Livro, Romancista
from sqlalchemy import select


def test_create_user(session):

    user = User(username='romario', password='password',
                email='romario@email.com')

    session.add(user)
    session.commit()

    result = session.scalar(
        select(User).where(User.email == 'romario@email.com')
    )

    assert result.username == 'romario'


def test_create_romancista(session):

    romancista = Romancista(nome='machado de assis')

    session.add(romancista)
    session.commit()
    session.refresh(romancista)

    assert romancista.id == 1


def test_create_liro(session):

    romancista = Romancista(nome='machado de assis')

    session.add(romancista)
    session.commit()
    session.refresh(romancista)

    livro = Livro(ano=datetime.now(), titulo='dom casmurro', id_romancista=1)

    session.add(livro)
    session.commit()
    session.refresh(livro)

    assert livro.id == 1
