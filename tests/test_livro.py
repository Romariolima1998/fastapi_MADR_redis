from http import HTTPStatus


# ########################### post ########################################
def test_create_livro(client, token, romancista):
    response = client.post(
        '/livros',
        headers={'authorization': f'Bearer {token}'},
        json={
            "ano": 0,
            "titulo": "test",
            "id_romancista": romancista.id
        }
    )

    livro = response.json()

    assert response.status_code == HTTPStatus.CREATED
    assert livro == {"id": 1, "ano": 0000,
                     "titulo": "test", "id_romancista": romancista.id}


def test_exception_create_livro_id_romancista_not_exists(client, token,):
    response = client.post(
        '/livros',
        headers={'authorization': f'Bearer {token}'},
        json={
            "ano": 0,
            "titulo": "test",
            "id_romancista": 0
        }
    )

    livro = response.json()

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert livro['detail'] == 'romancista_id nao coincide com nenhum romancista'


def test_exception_create_livro_exists(client, token, livro, romancista):
    response = client.post(
        '/livros',
        headers={'authorization': f'Bearer {token}'},
        json={
            "ano": 0,
            "titulo": livro.titulo,
            "id_romancista": romancista.id
        }
    )

    livro = response.json()

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert livro['detail'] == 'livro já consta no MADR'


# ####################### get ###############################################


def test_read_livro_id(client, livro):
    response = client.get(
        f'/livros/{livro.id}'
    )

    livro_ = response.json()

    assert response.status_code == HTTPStatus.OK
    assert livro_ == {
        'id': livro.id,
        'ano': livro.ano,
        'titulo': livro.titulo,
        'id_romancista': livro.id_romancista
    }


def test_exception_read_livro_not_exists_id(client):
    response = client.get(
        '/livros/0'
    )

    livro_ = response.json()

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert livro_['detail'] == "Livro não consta no MADR"


def test_read_livro_query(client, livro):
    response = client.get(
        f'/livros?nome={livro.titulo}'
    )

    livro_ = response.json()

    assert response.status_code == HTTPStatus.OK
    assert livro_ == {'livros': [{
        'id': livro.id,
        'ano': livro.ano,
        'titulo': livro.titulo,
        'id_romancista': livro.id_romancista
    }]}


def test_read_not_livro_query(client):
    response = client.get(
        '/livros?nome=a'
    )

    livro_ = response.json()

    assert response.status_code == HTTPStatus.OK
    assert livro_ == {'livros': []}

# ########################### patch ###################################


def test_update_livro(client, livro, token):
    response = client.patch(
        f'/livros/{livro.id}',
        headers={'authorization': f'Bearer {token}'},
        json={
            "ano": 2024
        }
    )

    livro_ = response.json()

    assert response.status_code == HTTPStatus.OK
    assert livro_ == {
        'id': livro.id,
        'ano': 2024,
        'titulo': livro.titulo,
        'id_romancista': livro.id_romancista
    }


def test_exception_update_livro_not_exists(client, token):
    response = client.patch(
        '/livros/0',
        headers={'authorization': f'Bearer {token}'},
        json={
            "ano": 2024
        }
    )

    livro_ = response.json()

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert livro_['detail'] == 'Livro não consta no MADR'


# ############################ delete ###########################################

def test_delete_livro(client, livro, token):
    response = client.delete(
        f'/livros/{livro.id}',
        headers={'authorization': f'Bearer {token}'},
    )

    livro_ = response.json()

    assert response.status_code == HTTPStatus.OK
    assert livro_ == {'message': "Livro deletado no MADR"}


def test_exception_delete_livro_not_exists(client, token):
    response = client.delete(
        '/livros/0',
        headers={'authorization': f'Bearer {token}'},
    )

    livro_ = response.json()

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert livro_['detail'] == 'Livro não consta no MADR'
