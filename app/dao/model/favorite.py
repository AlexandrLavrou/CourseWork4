from marshmallow import Schema, fields

from app.dao.model.movie import MovieSchema
from app.dao.model.user import UserSchema
from app.setup_db import db


class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"))
    user = db.relationship("User")
    movie = db.relationship("Movie")


class FavoriteSchema(Schema):
    user_id = fields.Int()
    movie_id = fields.Int()
    user = fields.Pluck(UserSchema, 'name')
    movie = fields.Pluck(MovieSchema, 'title')
