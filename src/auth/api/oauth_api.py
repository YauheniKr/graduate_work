from http import HTTPStatus

from authlib.integrations.flask_client import OAuth
from flask import Blueprint
from flask import current_app as app
from flask import make_response, url_for
from flask_restful import Api, Resource

from core.config import settings

oauth = OAuth(app)

oauth_blueprint = Blueprint('oauth', __name__)
oauth_api = Api(oauth_blueprint, prefix='/api/v1/auth')

access_data = {
    'grant_type': 'authorization_code',
    'client_id': settings.YANDEX_ID,
    'client_secret': settings.YANDEX_PASSWORD,
}

oauth.register('yandex', client_id=settings.YANDEX_ID, client_secret=settings.YANDEX_PASSWORD,
               authorize_url='https://oauth.yandex.ru/authorize', access_token_url='https://oauth.yandex.ru/token',
               access_token_params=access_data, userinfo_endpoint='https://login.yandex.ru/info',)


class YandexLogin(Resource):

    def get(self, social_name: str):
        client = oauth.create_client(social_name)
        if not client:
            return make_response({'msg': f'{client} not found'}, HTTPStatus.NOT_FOUND)
        redirect_url = url_for(
            "oauth.oauthauthorization", social_name=social_name, _external=True,
        )
        return client.authorize_redirect(redirect_url)


oauth_api.add_resource(YandexLogin, '/oauth/login/<string:social_name>')
