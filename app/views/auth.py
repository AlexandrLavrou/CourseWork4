from flask import request
from flask_restx import Resource, Namespace

from app.container import auth_service

auth_ns = Namespace('auth')


@auth_ns.route('/register/')
class AuthRegisterView(Resource):
    def post(self):
        auth_service.register_user(request.json)
        return "", 201


@auth_ns.route('/login/')
class AuthLoginView(Resource):
    def post(self):
        user_data = request.json
        email = user_data.get('email')
        password = user_data.get('password')
        if None in [email, password]:
            return "Не введен логин или пароль", 400

        tokens = auth_service.generate_tokens(email, password)
        if tokens:
            return tokens, 201
        else:
            return "Ошибка в запросе", 400

    def put(self):
        data = request.json
        token = data.get('refresh_token')
        return auth_service.approve_refresh_token(token)
