from flask import Flask
from flask_cors import CORS
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # enable CORS
    CORS(app)

    # 注册 blueprint
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
