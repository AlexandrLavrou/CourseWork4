from flask import request
from flask_restx import Namespace, Resource

from app.container import user_service, users_schema, user_schema
from app.helpers.decorators import admin_required

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):

    def get(self):
        users = user_service.get_all()
        res = users_schema(many=True).dump(users)
        return res, 200

    def post(self):
        req_json = request.json
        user = user_service.create(req_json)
        return "", 201, {"location": f"/users/{user.id}"}


@user_ns.route('/<int:bid>')
class UserView(Resource):
    def get(self, bid):
        b = user_service.get_one(bid)
        sm_d = user_schema().dump(b)
        return sm_d, 200

    def put(self, bid):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = bid
        user_service.update(req_json)
        return "", 204

    @admin_required
    def delete(self, bid):
        user_service.delete(bid)
        return "", 204
