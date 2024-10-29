import pytest

from fastapi.testclient import TestClient

import factory
import factory.fuzzy
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from madr.database import get_session
from madr.app import app
from madr.models import User, Romancista, Livro, table_registry
from madr.security import get_password_hash
# from fast_zero.settings import Settings


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}password')\



@pytest.fixture()
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override

        yield client

    app.dependency_overrides.clear()

# with PostgresContainer('postgres:16', driver='psycopg') as postgres:
#     engine = create_engine(postgres.get_connection_url())


@pytest.fixture(scope='session')
def engine():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False}, poolclass=StaticPool,
    )

    with engine.begin():
        yield engine


@pytest.fixture()
def session(engine):

    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def user(session: Session):
    pwd = 'test'
    user = UserFactory(password=get_password_hash(pwd))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = pwd
    return user


@pytest.fixture
def other_user(session: Session):
    pwd = 'test'
    user = UserFactory(password=get_password_hash(pwd))

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        'auth/token/',
        data={'username': user.username, 'password': user.clean_password},
    )
    return response.json()['access_token']


@pytest.fixture
def romancista(session: Session):
    _romancista = Romancista(nome='test')

    session.add(_romancista)
    session.commit()
    session.refresh(_romancista)

    return _romancista


@pytest.fixture
def livro(session, romancista):

    _livro = Livro(ano=0000, titulo='test', id_romancista=romancista.id)

    session.add(_livro)
    session.commit()
    session.refresh(_livro)

    return _livro
