from contextlib import suppress
from typing import Dict, List, Any, Type

from sqlalchemy.exc import IntegrityError


from app.dao.model.director import Director
from app.dao.model.genre import Genre
from app.dao.model.movie import Movie
from app.dao.model.user import User
from app.setup_db import db
from app.utils import read_json
from main import app


def load_data(data, model) -> None:
    for item in data:
        item['id'] = item.pop('pk')
        db.session.add(model(**item))


if __name__ == '__main__':
    fixtures: Dict[str, List[Dict[str, Any]]] = read_json("fixtures.json")

    # app = create_app(config)

    with app.app_context():

        load_data(fixtures['genres'], Genre)
        load_data(fixtures['directors'], Director)
        load_data(fixtures['movies'], Movie)
        load_data(fixtures['users'], User)
        with suppress(IntegrityError):
            db.session.commit()
