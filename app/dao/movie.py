from app.dao.model.movie import Movie
from constants import QUANTITY_LIST


class MovieDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, mid):
        return self.session.query(Movie).get(mid)

    def get_all(self, page=None, status=None):
        offset_list = None
        quantity_list = None
        if page:
            offset_list = (int(page) - 1) * QUANTITY_LIST
            quantity_list = QUANTITY_LIST
        if status == 'new':
            return self.session.query(Movie).order_by(Movie.year).offset(offset_list).limit(quantity_list).all()
        else:
            return self.session.query(Movie).all()
