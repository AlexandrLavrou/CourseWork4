from flask import request
from flask_restx import Namespace, Resource

from app.container import movie_service

from app.dao.model.movie import MovieSchema
from app.helpers.decorators import auth_required, admin_required

movie_ns = Namespace('movies')


@movie_ns.route('/')
class MoviesView(Resource):

    @auth_required
    def get(self):
        rs = movie_service.get_all()
        res = MovieSchema(many=True).dump(rs)
        return res, 200

    # @admin_required
    # def post(self):
    #     req_json = request.json
    #     movie = movie_service.create(req_json)
    #     return "", 201, {"location": f"/movie/{movie.id}"}


@movie_ns.route('/<int:did>')
class MovieView(Resource):
    @auth_required
    def get(self, did):
        r = movie_service.get_one(did)
        sm_d = MovieSchema().dump(r)
        return sm_d, 200

    # @admin_required
    # def put(self, did):
    #     req_json = request.json
    #     if "id" not in req_json:
    #         req_json["id"] = did
    #     movie_service.update(req_json)
    #     return "", 204
    #
    # @admin_required
    # def delete(self, did):
    #     movie_service.delete(did)
    #     return "", 204
