
from flask_jwt import jwt_required,JWTError,JWT
from flask import app,jsonify,redirect
from flask_restful import Resource,reqparse, Api
from models.user import User
import datetime
import models.user_token
from werkzeug.security import safe_str_cmp
from collections import OrderedDict

parser = reqparse.RequestParser()
parser.add_argument("username",type=str,location = "json")
parser.add_argument("password",type=str,location = "json")


class LoginCredentials(Resource):
    def __init__(self,id,username, password):
        self.id = id;
        self.username = username;
        self.password = password;

    def authenticate(username, password):
        for user in User.objects().filter(username=username):
            if user.password == password:
                return LoginCredentials(str(user.id),user.username,user.password)

    def identity(payload):
        user_id = payload["identity"]
        user = User.objects().with_id(user_id)
        if (user_id is not None):
            return LoginCredentials(str(user.id),user.username, user.password)

def handle_user_exception_again(e):
    if isinstance(e, JWTError):
        return jsonify(OrderedDict([
            ('status_code', e.status_code),
            ('error', e.error),
            ('description', e.description),
        ])), e.status_code, e.headers
    return e

class RegisterRes(Resource):
    def post(self):
        args = parser.parse_args()
        username = args["username"]
        password = args["password"]

        found_user = User.objects(username = username).first()
        if found_user is not None:
            return {"code":0,"Message":"User already exists", "token":""}, 400
        user = User(username = username, password = password)
        user.save()
        return redirect('/login', 307)


def authenticate(username, password):
    print("Authenticate register")
    for user in User.objects(username=username):
        if user.password == password:
            if safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
                print("OK")
                return LoginCredentials(str(user.id), user.username, user.password)

def identity(payload):
    print("Identity register")
    user_id = payload['identity']
    user = User.objects.with_id(user_id)
    if user is not None:
        return LoginCredentials(str(user.id), user.username, user.password)

def jwt_init(app):
    app.config['SECRET_KEY'] = 'khanh'
    app.config["JWT_EXPIRATION_DELTA"] = datetime.timedelta(hours = 24)
    app.config["JWT_AUTH_URL_RULE"] = "/login"
    # Catch exception and return it to users
    # https://github.com/mattupstate/flask-jwt/issues/32
    app.handle_user_exception = handle_user_exception_again
    jwt = JWT(app=app,
              authentication_handler=authenticate,
              identity_handler=identity)
    return jwt