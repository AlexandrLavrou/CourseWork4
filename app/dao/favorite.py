from app.dao.model.favorite import Favorite
from app.dao.model.movie import Movie


class FavoriteDAO:
    def __init__(self, session):
        self.session = session

    def get_favorite(self, uid, mid):

        data = self.session.query(Favorite) \
            .filter(Favorite.user_id == uid, Favorite.movie_id == mid) \
            .all()
        return data

    def get_user_favorites(self):

        data = self.session.query(Movie).join(Favorite).all()
        return data

    def create(self, data):

        ent = Favorite(**data)
        self.session.add(ent)
        self.session.commit()
        return ent

    def delete(self, uid):
        item = self.session.query(Favorite).get(uid)
        self.session.delete(item)
        self.session.commit()
