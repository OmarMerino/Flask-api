# from decouple import config
# from decouple import config as decouple_config
import os
import psycopg2
import traceback
from dotenv import load_dotenv
# Logger
from src.utils.Logger import Logger
load_dotenv()  # Cargar variables de entorno desde .env


def get_connection():
    try:
        
        return psycopg2.connect(
            host=os.environ.get('POSTGRES_HOST'),
            port=os.environ.get('POSTGRES_PORT'),
            user=os.environ.get('POSTGRES_USER'),
            password=os.environ.get('POSTGRES_PASSWORD'),
            database=os.environ.get('DB')
        )
    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())