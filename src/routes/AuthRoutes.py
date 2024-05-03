from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity


import traceback

# Logger
from src.utils.Logger import Logger
# Models
from src.models.UserModel import User
# Security
from src.utils.Security import Security
# Services
from src.services.AuthService import AuthService

main = Blueprint('auth_blueprint', __name__)


@main.route('/login', methods=['POST'])
def login():
    try:
        username = request.json['username']
        password = request.json['password']
        _user = User(None, username, password)
        
        #verificamos el usuario
        authenticated_user = AuthService.login_user(_user)

        #entregamos token si el servicio autentica
        if (authenticated_user):
            encoded_token = Security.generate_token(_user)
            return jsonify({'success': True, 'token': encoded_token})
        else:
            response = jsonify({'message': 'Unauthorized'})
            return response, 401
        
    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())

        return jsonify({'message': "ERROR", 'success': False})
    

    
@main.route('/register', methods=['POST'])
def register():
    try:
        username = request.json['username']
        password = request.json['password']
        if not username or not password:
            return jsonify({'message': 'Se requiere un nombre de usuario y una contraseña.'}), 400
        

        user = User(0, username, password)

        if AuthService.register_user(user):
            return jsonify({'message': 'Usuario registrado correctamente'}), 201
        else:
            return jsonify({'message': 'Error durante el registro'}), 400
    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': 'Error durante el registro'}), 500

# Protege una  xruta con jwt_required, bloquea las peticiones sin un JWT válido
@main.route("/", methods=["POST"])
@jwt_required()
def autenticate():
    print("Autenticacion de usuario:")
    # Accede a la identidad del usuario actual con get_jwt_identity
    current_user = get_jwt_identity()
    print(current_user)
    
    return jsonify({"username": current_user }), 200
