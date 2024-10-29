from jwt import decode

from madr.security import create_access_token, settings


def test_create_token_jwt():
    data = {'sub': 'test@test.com'}
    token = create_access_token(data)

    result = decode(token, settings.SECRET_KEY,
                    algorithms=[settings.ALGORITHM])

    assert result['sub'] == data['sub']
    assert result['exp']
