from app.dao.favorite import FavoriteDAO
from app.dao.genre import GenreDAO
from app.dao.director import DirectorDAO
from app.dao.model.favorite import FavoriteSchema
from app.dao.user import UserDAO
from app.dao.movie import MovieDAO

from app.dao.model.director import DirectorSchema
from app.dao.model.genre import GenreSchema
from app.dao.model.movie import MovieSchema
from app.dao.model.user import UserSchema
from app.service.auth import AuthService

from app.service.director import DirectorService
from app.service.favorite import FavoriteService
from app.service.genre import GenreService
from app.service.movie import MovieService
from app.service.user import UserService

from app.setup_db import db

director_dao = DirectorDAO(session=db.session)
director_service = DirectorService(dao=director_dao)
director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)

genre_dao = GenreDAO(session=db.session)
genre_service = GenreService(dao=genre_dao)
genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)

movie_dao = MovieDAO(session=db.session)
movie_service = MovieService(dao=movie_dao)
movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

user_dao = UserDAO(session=db.session)
user_service = UserService(dao=user_dao)
user_schema = UserSchema()
users_schema = UserSchema(many=True)

auth_service = AuthService(dao=user_dao)

favorite_dao = FavoriteDAO(session=db.session)
favorite_service = FavoriteService(dao=favorite_dao)
favorite_schema = FavoriteSchema()
favorites_schema = FavoriteSchema(many=True)

