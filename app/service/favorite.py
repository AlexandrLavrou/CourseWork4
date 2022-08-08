from flask_restx import abort

from app.dao.favorite import FavoriteDAO


class FavoriteService:
    def __init__(self, dao: FavoriteDAO):
        self.dao = dao

    def add_favourite(self, user_id, movie_id) -> object:

        data = {
            'user_id': user_id,
            'movie_id': movie_id
        }
        if self.dao.get_favorite(user_id, movie_id):
            raise 404

        return self.dao.create(data)

    def get_user_favorites(self):
        favourites = self.dao.get_user_favorites()
        return favourites

    def delete_favourite(self, user_id, movie_id):
        favourite = self.dao.get_favorite(user_id, movie_id)

        if not favourite:
            abort(404)
        self.dao.delete(favourite[0].id)
