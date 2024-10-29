from http import HTTPStatus


# ##########################post#########################################

def test_create_romancista(client, token):

    response = client.post(
        '/romancista',
        headers={'authorization': f'Bearer {token}'},
        json={
            'nome': 'test'
        }
    )

    romancista = response.json()

    assert response.status_code == HTTPStatus.CREATED
    assert romancista['id'] == 1


def test_create_exception_romancista_exists(client, token, romancista):

    response = client.post(
        '/romancista',
        headers={'authorization': f'Bearer {token}'},
        json={
            'nome': 'test'
        }
    )

    romancista = response.json()

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert romancista['detail'] == 'romancista já consta no MADR'

    # #################################get###################################


def test_read_romancista_id(client, romancista):
    response = client.get(
        f'/romancista/{romancista.id}'
    )

    romancista_ = response.json()

    assert response.status_code == HTTPStatus.OK
    assert romancista_ == {
        'id': 1,
        'nome': 'test'
    }


def test_read_romancista_id_not_exists(client, romancista):
    response = client.get(
        f'/romancista/{5}'
    )

    romancista_ = response.json()

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert romancista_['detail'] == "Romancista não consta no MADR"


def test_read_romancista_query(client, romancista):
    response = client.get(
        f'/romancista?nome={romancista.nome}'
    )

    romancista_ = response.json()

    assert response.status_code == HTTPStatus.OK
    assert romancista_ == {'romancistas': [{
        'id': 1,
        'nome': 'test'
    }]}


def test_read_romancista_query_empty_list(client):
    response = client.get(
        '/romancista?nome=a'
    )

    romancista_ = response.json()

    assert response.status_code == HTTPStatus.OK
    assert romancista_ == {'romancistas': []}


# ##############################patch############################


def test_update_romancista(client, token, romancista):

    response = client.patch(
        f'/romancista/{romancista.id}',
        headers={'authorization': f'Bearer {token}'},
        json={
            'nome': 'test1'
        }
    )

    romancista = response.json()

    assert response.status_code == HTTPStatus.OK
    assert romancista == {
        'id': 1,
        'nome': 'test1'
    }


def test_exception_update_romancista_not_exists(client, token,):

    response = client.patch(
        '/romancista/5',
        headers={'authorization': f'Bearer {token}'},
        json={
            'nome': 'test1'
        }
    )

    romancista = response.json()

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert romancista['detail'] == 'Romancista não consta no MADR'

    # ########################delete###############################


def test_delete_romancista(client, token, romancista):

    response = client.delete(
        f'/romancista/{romancista.id}',
        headers={'authorization': f'Bearer {token}'},

    )

    romancista_ = response.json()

    assert response.status_code == HTTPStatus.OK
    assert romancista_ == {'message': 'Romancista deletada no MADR'}


def test_exception_delete_romancista_not_exists(client, token):

    response = client.delete(
        '/romancista/5',
        headers={'authorization': f'Bearer {token}'},

    )

    romancista = response.json()

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert romancista['detail'] == 'Romancista não consta no MADR'
