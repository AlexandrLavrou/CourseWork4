from app.dao.model.user import User
from constants import QUANTITY_LIST


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, uid):
        return self.session.query(User).get(uid)

    def get_all(self, page=None):
        if page:
            offset_list = (int(page) - 1) * QUANTITY_LIST
            quantity_list = QUANTITY_LIST
            return self.session.query(User).order_by(User.id).offset(offset_list).limit(quantity_list).all()
        else:
            return self.session.query(User).all()

    def get_by_email(self, email):
        try:
            user = self.session.query(User).filter(User.email == email.strip()).one()
            return user
        except Exception:
            return False

    def create(self, user_data):
        ent = User(**user_data)
        self.session.add(ent)
        self.session.commit()
        return ent

    def update(self, user_data):
        user = self.get_one(user_data.get("id"))
        if not user:
            return False
        if user_data.get("email"):
            user.email = user_data.get("email")
        if user_data.get("password"):
            user.password = user_data.get("password")
        if user_data.get("name"):
            user.name = user_data.get("name")
        if user_data.get("surname"):
            user.surname = user_data.get("surname")
        if user_data.get("favorite_genre"):
            user.favorite_genre = user_data.get("favorite_genre")

        self.session.add(user)
        self.session.commit()

    def put(self, user):
        self.session.add(user)
        self.session.commit()
