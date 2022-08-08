from app.dao.model.genre import Genre

from constants import QUANTITY_LIST


class GenreDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, mid):
        return self.session.query(Genre).get(mid)

    def get_all(self, page=None):
        if page:
            offset_list = (int(page) - 1) * QUANTITY_LIST
            quantity_list = QUANTITY_LIST
            return self.session.query(Genre).order_by(Genre.id).offset(offset_list).limit(quantity_list).all()
        else:
            return self.session.query(Genre).all()
