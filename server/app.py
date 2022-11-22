from flask import Flask
from flask_restful import Api
from db import db
import logging
from logging import handlers
import os
from flask.logging import default_handler

app = Flask(__name__)
api = Api(app)

app.config["MONGODB_SETTINGS"] = [
    {
        "db": "message_db",
        "host": "mongodb",
        "port": 27017,
    }   
]
app.config["LOG_TYPE"] = os.environ.get("LOG_TYPE", "watched")
app.config["LOG_LEVEL"] = os.environ.get("LOG_LEVEL", "INFO")
app.config["LOG_FILE"] = os.environ.get("LOG_LEVEL", "info.log")
db.init_app(app)
# Tạo config logging
# [2021-12-22 15:30:09,980] INFO in home.py:10:get() -> {messages}
formatter = logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(filename)s:%(lineno)d:%(funcName)s()'
    ' -> %(message)s'
)
# apm_handler = LoggingHandler(client=apm.client)
file_handler = handlers.TimedRotatingFileHandler(
    app.config.get('LOG_FILE'),
    when="D",
    backupCount=30
)
file_handler.setFormatter(formatter)

app.logger.removeHandler(default_handler)
default_handler.setFormatter(formatter)

app.logger.addHandler(default_handler)
app.logger.addHandler(file_handler)
# app.logger.addHandler(apm_handler)
app.logger.setLevel(logging.INFO)

from resources.message import SendMessage
api.add_resource(SendMessage, '/messages')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

