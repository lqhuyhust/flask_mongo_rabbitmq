from flask import jsonify, render_template, make_response
from flask import current_app as app

from flask_restful import Resource

from flask_babel import lazy_gettext as _l


class Index(Resource):

    def get(self, **kwargs):
        # Khởi tạo logging
        # {status_code} - {description}
        log_msg = '{status_code} - {description}'

        message = {
            "title": _l("API Dịch vụ Bizfly DNS"),
            "version": "v2.0",
            "author": _l("Hữu Tuấn Anh"),
            "email": _l("anhnguyenhuutuan@vccorp.vn"),
            "description": _l(
                "API cho phép người dùng thao tác với dịch vụ DNS"),
        }
        app.logger.info(log_msg.format(
            status_code=200,
            description='Success',
        ))
        return jsonify(message)


class DocsApi(Resource):

    def get(self, *args, **kwargs):
        url_doc = ''
        return make_response(render_template('index.html', url_doc=url_doc))
