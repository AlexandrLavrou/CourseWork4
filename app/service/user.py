import base64
import hashlib
import hmac

import jwt
from flask_restx import abort

from app.dao.user import UserDAO
from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS, JWT_ALGORITHM, JWT_SECRET


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_all(self, page_num):
        return self.dao.get_all(page_num)

    def create(self, user_data):
        user_data["password"] = self.generate_password(user_data["password"])
        return self.dao.create(user_data)

    def update(self, user_data):
        user_data["password"] = self.generate_password(user_data["password"])
        return self.dao.update(user_data)

    def get_id_by_token(self, data_headers):
        token = data_headers['Authorization'].split('Bearer ')[-1]
        data = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        uid = data['id']
        return uid

    def put(self, uid, user_data):
        user = self.get_one(uid)
        if not self.compare_password(user.password, user_data['old_password']):
            abort(400)
        user.password = self.get_hash(user_data['new_password'])
        self.dao.put(user)

    def get_hash(self, password):
        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )
        return base64.b64encode(hash_digest)

    def generate_password(self, password):
        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )

        return base64.b64encode(hash_digest)

    def compare_password(self, hash_password, other_password):
        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            other_password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )
        decoded_digest = base64.b64decode(hash_password)

        return hmac.compare_digest(decoded_digest, hash_digest)