from http import HTTPStatus

import backoff
import jwt

from fastapi import HTTPException, Depends
from fastapi.security import HTTPBasicCredentials, HTTPBearer
from urllib3.exceptions import MaxRetryError


class AuthApi:
    def __init__(self):
        pass

    @backoff.on_exception(backoff.expo, MaxRetryError, max_tries=3)
    def token_introspect(self, access_token: str):
        """
        Выполняет запрос к сервису Auth для проверки актуальности токена
        """
        # return self.api_instance.api_v1_token_introspect_post(body={'access_token': access_token})
        return {'active': True}


auth_api = AuthApi()

security = HTTPBearer()

credentials: HTTPBasicCredentials = Depends(security)


def get_current_user_id(required_roles: tuple = tuple()):

    async def func_wrapper(credentials: HTTPBasicCredentials = Depends(security)):
        access_token = credentials.credentials

        payload = jwt.decode(
            access_token,
            algorithms=['HS256'],
            options={'verify_signature': False},
        )
        token_roles = payload.get('roles', tuple())
        user_id = payload['sub']

        try:
            response = auth_api.token_introspect(access_token)
            if not response['active']:
                raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                    detail='Token is incorrect')
        except Exception as e:
            if e.status == HTTPStatus.BAD_REQUEST:
                raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                    detail='Token is incorrect')
        except MaxRetryError:
            raise HTTPException()

        for roles in required_roles:
            if roles not in token_roles:
                raise HTTPException(status_code=HTTPStatus.FORBIDDEN,
                                    detail='Authorization failed')
        return user_id

    return func_wrapper
