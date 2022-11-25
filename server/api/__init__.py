# -*- coding: utf-8 -*-
'''Khởi tạo package api. Cung cấp hàm create_app theo mô hình factory app.
Các thư mục có trong package:
    - app_config: Chứa các file config dùng cho api
    - commons: Các công cụ sử dụng để thao tác
    - models: Các model được sử dụng
    - resources: Các route api
    - templates: Các template dùng để render
    - translations: Các phiên bản dùng cho các ngôn ngữ khác
'''
import logging
from logging import handlers

from flask import Flask
from flask_mongoengine import MongoEngine
from flask.logging import default_handler
from flasgger import Swagger
from flask_cors import CORS
from flask_babel import Babel
from itsdangerous import URLSafeTimedSerializer

from api.commons.common_utils import get_timezone, get_locale
from api.commons.session_interface import ItsdangerousSessionInterface

# Khởi tạo swagger config
swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'message_docs_api',
            "route": '/message_docs_api.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "static_folder": "static",  # must be set by user
    "swagger_ui": False,
}
swagger = Swagger(
    config=swagger_config,
    template_file='templates/message_api.yaml',
    parse=True,
)
db = MongoEngine()
babel = Babel()


def create_app():
    '''Hàm khởi tạo một app Api mới.
    Api được khởi tạo theo thứ tự:
        - Đọc config từ pyfile
        - Khởi tạo logger và formatter
        - cookie serializer
        - cors
        - DB
        - Thiết lập cài đặt cho i18n
        - Thiết lập auto gen docs api

    Args:
    Returns:
        App đã được khởi tạo
    Raises:
    '''
    app = Flask(__name__)

    app.config.from_pyfile('app_config/base.py')

    # Tạo config logging
    # [2021-12-22 15:30:09,980] INFO in home.py:10:get() -> {messages}
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(filename)s:%(lineno)d:%(funcName)s()'
        ' -> %(message)s'
    )
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
    app.logger.setLevel(logging.INFO)

    # Use custom session interface
    app.config['COOKIE_SERIALIZER'] = URLSafeTimedSerializer(
        app.secret_key,
        signer_kwargs={'key_derivation': 'hmac'})
    app.session_interface = ItsdangerousSessionInterface()

    # CORS
    CORS(app, supports_credentials=True)

    # Init database connect
    db.init_app(app)

    # Init i18n
    babel.init_app(app)
    babel.localeselector(get_locale)
    babel.timezoneselector(get_timezone)

    # Create autogen docs
    app.config['SWAGGER'] = {
        'uiversion': 3,
        'openapi': '3.0.2',
    }

    # Init auto gen docs
    swagger.init_app(app)

    return app
