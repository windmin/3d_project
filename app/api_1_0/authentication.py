from flask import g, jsonify
#蓝本
from . import api
#数据库
from ..models import User, AnonymousUser
from .errors import forbidden, unauthorized

from flask_httpauth import HTTPBasicAuth


auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    if username == '':
        g.current_user = AnonymousUser()
        return True
    user = User.query.filter_by(username=username).first()
    if not user:
        return False
    g.current_user = user
    return user.verify_password(password)


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')


@api.before_request
@auth.login_required
def before_request():
    if not g.current_user.is_anonymous and \
            not g.current_user.confirmed:
        return forbidden('Unconfirmed account')