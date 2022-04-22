from http import HTTPStatus

from flasgger import Swagger
from flask import Flask, make_response, request
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from api.oauth_api import oauth_blueprint
from api.payment_api import payment_blueprint
from api.role_api import roles_blueprint, roles_status_blueprint
from api.user_api import token_blueprint, user_blueprint
from core.config import settings

from .commands import usersbp

app = Flask(__name__)
swagger = Swagger(app)
app.config['JWT_SECRET_KEY'] = settings.SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = settings.ACCESS_EXPIRES
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = settings.REFRESH_EXPIRES
app.config["SECRET_KEY"] = settings.SECRET_KEY

jwt = JWTManager(app)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=['200 per day', '50 per hour']
)
limiter.limit('10 per second')(roles_status_blueprint)

app.register_blueprint(usersbp)
app.register_blueprint(roles_blueprint)
app.register_blueprint(roles_status_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(token_blueprint)
app.register_blueprint(oauth_blueprint)
app.register_blueprint(payment_blueprint)

from flask_opentracing import FlaskTracer
from jaeger_client import Config


@app.before_request
def before_request():
    request_id = request.headers.get('X-Request-Id')
    if not request_id:
        return make_response('X-Request-Id not found', HTTPStatus.NOT_FOUND)


config_data = {
    'sampler': {
        'type': 'const',
        'param': 1,
    },
    'local_agent': {
        'reporting_host': 'jaeger',
        'reporting_port': '6831',
    },
    'logging': True,
}


def _setup_jaeger():
    config = Config(config=config_data, service_name="movies-api", validate=True, )
    return config.initialize_tracer()


tracer = FlaskTracer(_setup_jaeger, app=app)

if __name__ == '__main__':
    app.run()
