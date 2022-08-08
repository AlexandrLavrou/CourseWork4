import base64
import hmac
import datetime
import calendar
from hashlib import pbkdf2_hmac

import jwt
from flask_restx import abort

from app.dao.user import UserDAO
from constants import JWT_ALGORITHM, JWT_SECRET, PWD_HASH_SALT, PWD_HASH_ITERATIONS





class AuthService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def register_user(self, user_data):
        email = user_data.get('email')
        password = user_data.get('password')
        if not email:
            return "input email"
        if not password:
            return "input password"
        result = self.verify_user(email)
        if result:
            return "email already exists"

        user_data['password'] = self.get_hash(password)
        return self.dao.create(user_data)

    def verify_user(self, email):
        if len(email.split('@')) < 2 or '.' not in email.split('@')[-1]:
            return "invalid email"
        return self.dao.get_by_email(email)

    def get_hash(self, password):
        hash_digest = pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )
        return base64.b64encode(hash_digest)

    def compare_passwords(self, password_hashed, password) -> bool:
        digest_decoded = base64.b64decode(password_hashed)
        digest_hashed = pbkdf2_hmac('sha256',
                                password.encode('utf-8'),
                                PWD_HASH_SALT,
                                PWD_HASH_ITERATIONS)

        return hmac.compare_digest(digest_decoded, digest_hashed)

    def generate_token(self, email, password, is_refresh=False):
        user = self.dao.get_by_email(email)
        if not user:
            abort(400)
            # return "user not found"

        if not is_refresh:
            if not self.compare_passwords(user.password, password):
                abort(400)

        data = {
            "id": user.id,
            "email": email
        }
        min30 = datetime.datetime.now() + datetime.timedelta(minutes=30)
        data['exp'] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

        days130 = datetime.datetime.now() + datetime.timedelta(days=130)
        data['exp'] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

    def approve_refresh_token(self, token):
        data = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        email = data['email']
        return self.generate_token(email, None, is_refresh=True)


def check_token(token):
    decoded_token = {}
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return True
    except Exception:
        abort(401)
    return decoded_token
