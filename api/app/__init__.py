from flask import Flask
from .database import db
from config import DevelopmentConfig
from flask_restful import Api
from flask_cors import CORS
import os

from flask import jsonify
from werkzeug.exceptions import HTTPException

if os.environ['MODE'] == 'DEV':
    from config import DevelopmentConfig as config
elif os.environ['MODE'] == 'PROD':
    from config import ProductionConfig as config

# blueprints
from .accounts import accounts_bp


def create_app():
    app = Flask(__name__)
    cors = CORS(app, resources={r"api/v1/accounts/*": {"origins": "*"}})
    app.config.from_object(config)
    app.register_blueprint(accounts_bp)
    api = Api(app)
    db.init_app(app)

    @app.errorhandler(Exception)
    def handle_error(e):
        code = 500
        if isinstance(e, HTTPException):
            code = e.code
        return jsonify(error=str(e)), code

    with app.test_request_context():
        db.create_all()
    return app
