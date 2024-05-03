import traceback

from src.db.db_postgres import get_connection

from src.utils.Logger import Logger

from src.models.UserModel import User

from src.utils.Security import Security

# Verificacion de password
class AuthService():


    @classmethod
    def login_user(cls, user):
        try:
            connection = get_connection()
            # RECUPERAR CONTRASEÑA ENCRIPTADA SI EXISTE EL USUARIO
            with connection.cursor() as cursor:

                cursor.execute('SELECT password FROM users WHERE username = %s', (user.username,))
                row = cursor.fetchone()

                
                if row is not None:
                    # si existe el usuario entonces comparamos las contraseñas utilizando bcrypt
                    return Security.compare(user.password,row[0])
                else:
                    return False

        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())




    @classmethod
    def register_user(cls, user):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                # Consulta SQL para insertar un nuevo usuario
                # Se realiza insercion mientras no exista un mismo username con condicion unique en la base de datos
                sql = """
                    INSERT INTO users (username, password)
                    VALUES (%s, %s)
                """
                # encriptar password con bcrypt
                hashed_password = Security.encrypt(user.password) 
                

                hashed_password_str = hashed_password.decode('utf-8')  # Convertir a cadena de texto

                values = (user.username,hashed_password_str)
                cursor.execute(sql, values)

                connection.commit()
                connection.close()

                rows_affected = cursor.rowcount  
                if rows_affected > 0:
                    return True
                else: 
                    return False
                


        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return False

        
        
