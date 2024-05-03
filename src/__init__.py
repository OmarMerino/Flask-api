from flask import Flask
from flask_jwt_extended import JWTManager
import os
# Routes
from .routes import AuthRoutes

app = Flask(__name__)

#configuracion de jwt
app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_KEY')
jwt = JWTManager(app)



def init_app(config):
    # Configuration
    app.config.from_object(config)

    # Blueprints
    app.register_blueprint(AuthRoutes.main, url_prefix='/auth')

    return app