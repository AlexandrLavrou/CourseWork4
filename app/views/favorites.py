from flask import request
from flask_restx import Namespace, Resource

from app.container import favorite_service, movies_schema
from app.service.auth import check_token


favourite_ns = Namespace('favorites')


@favourite_ns.route('/movies/')
class FavouriteMovies(Resource):

    def get(self):
        rs = favorite_service.get_user_favorites()
        res = movies_schema.dump(rs)
        return res, 200


@favourite_ns.route('/movies/<int:mid>/')
class FavouriteMovie(Resource):

    def post(self, mid):
        token = request.headers["Authorization"].split("Bearer ")[-1]
        access_token = check_token(token)["id"]
        favorite_service.add_favourite(access_token, mid)
        return "", 201

    def delete(self, mid):

        token = request.headers["Authorization"].split("Bearer ")[-1]
        email = check_token(token)["id"]
        favorite_service.delete_favourite(email, mid)
        return "", 200