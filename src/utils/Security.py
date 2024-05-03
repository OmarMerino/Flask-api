# from decouple import config
import bcrypt
import datetime
import pytz
import traceback
import os
# Logger
from src.utils.Logger import Logger
# jwt
from flask_jwt_extended import create_access_token



class Security():

    secret = os.environ.get('JWT_KEY')
    tz = pytz.timezone("America/Santiago")

    @classmethod
    def generate_token(cls, authenticated_user):
        print("generando token para: ", authenticated_user.username)
        try:
            payload = {
                'iat': datetime.datetime.now(tz=cls.tz),
                'exp': datetime.datetime.now(tz=cls.tz) + datetime.timedelta(minutes=10)
            }
            expires = datetime.timedelta(minutes=10)
            access_token = create_access_token(identity=authenticated_user.username, expires_delta=expires,additional_claims=payload)
            return access_token
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
    
    @staticmethod
    def encrypt(password):
        # Generar un hash con sal y costo de trabajo por defecto
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed_password

    @staticmethod
    def compare(password, hashed_password):
        # Comparar la contraseña ingresada con el hash almacenado
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))