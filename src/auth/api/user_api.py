from http import HTTPStatus

import opentracing
from flask import Blueprint, make_response, request
from flask_pydantic import validate
from flask_restful import Api, Resource
from jwt import ExpiredSignatureError

from src.db.global_init import create_session
from src.models.pydantic_models import AuthHistoryBase, AuthHistoryModel
from src.services.user import AuthHistoryRecord, TokenRequest, UserRequest
from src.services.utils import get_paginated_list

user_blueprint = Blueprint('user', __name__)
token_blueprint = Blueprint('token', __name__)
user_api = Api(user_blueprint, prefix='/api/v1/auth')
token_api = Api(token_blueprint, prefix='/api/v1/auth')


class UserCreate(Resource):

    def post(self):
        """
        Этот метод создает пользователя.
        ---
        tags:
          - User
        parameters:
          - name: body
            in: body
            schema:
              id: User
              properties:
                username:
                  type: string
                  required: true
                  description: имя пользователя
                password:
                  type: string
                  required: true
                  description: пароль пользователя
                email:
                  type: string
                  required: true
                  description: email пользователя

        responses:
          200:
            description: Пользователь создан
          409:
            description: Пользователь с данными параметрами уже существует
        """
        session = create_session()
        json_data = request.get_json(force=True)
        user = UserRequest(session)
        user = user.signup(json_data)
        if not user:
            return 'Пользователь с данными параметрами уже существует', HTTPStatus.CONFLICT
        session.close()
        return user


class UserLogin(Resource):

    def post(self):
        """
        Вход пользователя в аккаунт. В обмен на ввод пары login/password мы получаем 2 токена
        ---
        tags:
          - User
        parameters:
          - name: body
            in: body
            schema:
              properties:
                username:
                  type: string
                  required: true
                  description: имя пользователя
                password:
                  type: string
                  required: true
                  description: пароль пользователя

        responses:
          200:
            description: Succesfully logged
            schema:
              properties:
                access token:
                  type: string
                  description: access token
                refresh token:
                  type: string
                  description: refresh token
          404:
            description: User not found
          401:
            description: Пароль некорректен
        """
        from src.app import tracer
        parent_span = tracer.get_span()
        session = create_session()
        user = UserRequest(session)
        with opentracing.tracer.start_span(__name__, child_of=parent_span) as span:
            user = user.login()
        session.close()
        return user


class UserLogout(Resource):
    def get(self):
        """
        Выход пользователя из аккаунта.
        ---
        tags:
          - User
        parameters:
          - name: body
            in: header
            schema:
              properties:
                access_token:
                  type: string
                  required: true
                  description: токен доступа

        responses:
          200:
            description: Succesfully logged out
        """
        session = create_session()
        user = UserRequest(session)
        user = user.logout()
        session.close()
        return user


class UserUpdate(Resource):
    def patch(self):
        """
        Обновление информации о пользователе
        ---
        tags:
          - User
        parameters:
          - name: Authorization
            in: header
            schema:
              properties:
                access_token:
                  type: string
                  required: true
                  description: токен доступа. Добавляем Bearer в начало токена при тестировании
          - name: body
            in: body
            schema:
              id: User
              properties:
                username:
                  type: string
                  description: имя пользователя
                password:
                  type: string
                  description: пароль пользователя
                email:
                  type: string
                  description: email пользователя
        responses:
          200:
            description: User data updated
          400:
            description: User data incorrect
          404:
            description: User not found
        """
        json_data = request.get_json(force=True)
        session = create_session()
        user = UserRequest(session)
        user = user.update(json_data)
        return user


class GetUserAuthHistory(Resource):

    @validate(response_by_alias=True)
    def get(self):
        """
        Обновление информации о пользователе
        ---
        tags:
          - AuthHistory
        parameters:
          - name: page
            in: query
            schema:
              properties:
                page:
                  type: integer
                  description: Номер страницы
                  default: 1
          - name: limit
            in: query
            schema:
              properties:
                page:
                  type: integer
                  description: Количество записей на странице
                  default: 5
          - name: Authorization
            in: header
            schema:
              properties:
                access_token:
                  type: string
                  required: true
                  description: токен доступа. Добавляем Bearer в начало токена при тестировании
        responses:
          200:
            description: list of AuthHistory items
            schema:
              id: AuthHistoryModel
              properties:
                id:
                  type: string
                  description: идентификатор записи. Формат uuid4
                timestamp:
                  type: string
                  description:  дата входа в аккаунт
                user_agent:
                  type: string
                  description: описание программы с которого входили в аккаунт
                ip_address:
                  type: string
                  description: ip address устройства с которого входили в аккаунт
                device:
                  type: string
                  description: описание описание устройства с которго входили в аккаунт
        """
        session = create_session()
        auth_history = AuthHistoryRecord(session)
        try:
            auth_history = auth_history.get_auth_record()
            session.close()
        except ExpiredSignatureError:
            return make_response({'msg': 'token expired'}, 401)
        history = [AuthHistoryBase(id=record.id, timestamp=record.timestamp, user_agent=record.user_agent,
                                   ipaddress=record.ip_address, device=record.device)
                   for record in auth_history]

        auth_record_out = get_paginated_list(
            history,
            '/api/v1/auth/user/history',
            page=request.args.get('page', 1),
            limit=request.args.get('limit', 5)
        )
        return AuthHistoryModel(**auth_record_out)


class TokenRefresh(Resource):

    def post(self):
        """
        Обновление информации о пользователе
        ---
        tags:
          - User
        parameters:
          - name: Authorization
            in: header
            schema:
              properties:
                refresh_token:
                  type: string
                  required: true
                  description: токен обновления. Добавляем Bearer в начало токена при тестировании
        responses:
          200:
            description: Tokens updated
          401:
            description: Token is absent or incorrect
        """
        session = create_session()
        token = TokenRequest(session)
        token = token.refresh_token()
        return token


user_api.add_resource(UserCreate, '/user/signup/')
user_api.add_resource(UserLogin, '/user/login/')
user_api.add_resource(UserLogout, '/user/logout/')
user_api.add_resource(UserUpdate, '/user/me/')
user_api.add_resource(GetUserAuthHistory, '/user/history/')
token_api.add_resource(TokenRefresh, '/token/refresh/')
