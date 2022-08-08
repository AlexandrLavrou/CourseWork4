from app.dao.model.director import Director
from constants import QUANTITY_LIST


class DirectorDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, did):
        return self.session.query(Director).get(did)

    def get_all(self, page=None):
        if page:
            offset_list = (int(page) - 1) * QUANTITY_LIST
            quantity_list = QUANTITY_LIST
            return self.session.query(Director).order_by(Director.id).offset(offset_list).limit(quantity_list).all()
        else:
            return self.session.query(Director).all()

