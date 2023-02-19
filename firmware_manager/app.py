from flask import Flask
from flask_restful import Api

from firmware_manager.resources.firmware import Firmware
from firmware_manager.db.database import db


def create_app():
    flask_app = Flask(__name__)
    flask_app.config.from_pyfile("config.py")

    api = Api(flask_app)
    api.add_resource(Firmware, "/firmware/<device_id>")

    return flask_app


app = create_app()
db.init_app(app)
