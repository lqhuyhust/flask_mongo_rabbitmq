import json

from marshmallow import Schema, fields
from flask_restful import Resource
from flask import current_app as app
from flask import request, Response
from marshmallow import Schema, fields, validates, ValidationError
from marshmallow.validate import Length
from flask_babel import lazy_gettext as _l

from api.commons.message_utils import send_message
from api.model.message import Message
from api.commons.flasgger_marshmallow import swagger_decorator


class MessageCreateSchema(Schema):
    title = fields.String(
        required=True,
        allow_none=False,
        validate=Length(max=20, error=_l(
            "Tiêu đề cần ít hơn 20 ký tự").__str__()),
        doc='Tiêu đề  tin nhắn',
        example='Tin nhắn 1',
        error_messages={
            'required': _l('Tiêu đề là bắt buộc').__str__(),
        }
    )

    content = fields.String(
        required=True,
        allow_none=False,
        validate=Length(max=100, error=_l(
            "Nội dung cần ít hơn 100 ký tự").__str__()),
        doc='Nội dung tin nhắn',
        example='Mai đi chơi không?',
        error_messages={
            'required': _l('Nội dung là bắt buộc').__str__(),
        }
    )


class SuccessResponseSchema(Schema):
    '''Thành công'''
    status = fields.Boolean(
        required=True,
        doc="Trạng thái response",
        example=True
    )
    status_code = fields.String(
        required=True,
        doc="Status Code",
    )

    description = fields.String(
        required=True,
        doc="Mô tả response",
    )
    data = fields.Dict(
        required=False,
        doc="Dữ liệu trả ra sau khi gọi api",
        example={}
    )


class GetMessagesResponseSchema(SuccessResponseSchema):
    data = fields.Nested(
        MessageCreateSchema,
        many=True
    )
    status_code = fields.String(
        required=True,
        doc="Status Code",
        example="S001"
    )
    description = fields.String(
        required=True,
        doc="Mô tả response",
        example="Lấy danh sách tin nhắn thành công"
    )


class CreateMessageResponseSchema(SuccessResponseSchema):
    status_code = fields.String(
        required=True,
        doc="Status Code",
        example="S002"
    )
    description = fields.String(
        required=True,
        doc="Mô tả response",
        example="Tạo mới và gửi tin nhắn thành công"
    )


class ErrorResponseSchema(Schema):
    """Có lỗi xảy ra"""
    status = fields.Boolean(
        required=True,
        doc="Trạng thái response",
        example=False
    )

    status_code = fields.String(
        required=True,
        doc="Status Code",
    )

    description = fields.String(
        required=True,
        doc="Mô tả response",
    )
    data = fields.Dict(
        required=False,
        doc="Dữ liệu trả ra sau khi gọi api",
        example={}
    )


class ResponseDefaultSchema(Schema):
    '''<br><b>Mô tả status code</b><br>
    [200] Tạo mới tin nhắn và gửi đi thành công<br>
    [400] Trường title không được để trống<br>
    [400] Trường title không được vượt quá 20 ký tự<br>
    [400] Trường content không được để trống<br>
    [400] Trường content không được vượt quá 100 ký tự<br>
    [500] Có lỗi xảy ra trên hệ thống, vui lòng thử lại sau!<br>
    '''


class SendMessage(Resource):
    @ swagger_decorator(
        json_schema=MessageCreateSchema,
        description="""Thêm mới tin nhắn. Khi thêm mới thành công, tin nhắn sẽ được gửi đến tất cả các worker
        """,
        response_schema={
            '200': CreateMessageResponseSchema,
            '4xx': ErrorResponseSchema,
            '5xx': ErrorResponseSchema,
            'default': ResponseDefaultSchema,
        },
        tags=['Messages'],
    )
    def post(self, *args, **kwargs):
        """
        Tạo tin nhắn mới
        """
        # KHỞI TẠO LOGGING

        # {status_code} - {description}
        log_msg = '{status_code} - {description}'

        # ĐỌC THAM SỐ

        title = request.json.get('title')
        content = request.json.get('content')

        # KIỂM TRA THAM SỐ
        if not kwargs.get("validate_status"):
            description = f'Validate error: {kwargs["validate_message"]}'
            status_code = 400
            app.logger.info(log_msg.format(
                status_code=status_code,
                description=description,
            ))
            return Response(
                json.dumps({
                    'status': False,
                    'status_code': 'E001',
                    'description': description,
                    'data': {}
                }),
                status=status_code,
                content_type='application/json',
            )

        # LƯU MESSAGE VÀO DB

        message = Message(
            title=title,
            content=content,
        )
        message.save()

        # GỬI MESSAGE ĐẾN CÁC WORKER

        send_message(content)

        # Trả ra thông báo thành công

        status_code = 200
        description = _l('Gửi tin nhắn thành công').__str__()
        app.logger.info(log_msg.format(
            status_code=status_code,
            description=message,
        ))
        return Response(
            json.dumps({
                'status': True,
                'status_code': 'S001',
                'description': description,
                'data': {}
            }),
            status=status_code,
            content_type='application/json',
        )

    @swagger_decorator(
        description="""Lấy ra tất cả các tin nhắn đã được gửi
        """,
        response_schema={
            '200': GetMessagesResponseSchema,
            '500': ErrorResponseSchema,
            'default': ResponseDefaultSchema,
        },
        tags=['Messages'],
    )
    def get(request, *args, **kwargs):
        """
        Lấy ra tất cả các tin nhắn đã được gửi
        """
        # KHỞI TẠO LOGGING

        # {status_code} - {description}

        log_msg = '{status_code} - {description}'

        # LẤY DANH SÁCH MESSAGE

        # Lấy danh sách message từ DB

        try:
            messages = Message.objects()
        except Exception as error:
            status_code = 500
            description = _l('Có lỗi xảy ra trên hệ thống').__str__()
            app.logger.exception(log_msg.format(
                status_code=status_code,
                description=description,
            ))
            return Response(
                json.dumps({
                    'status': False,
                    'status_code': 'E101',
                    'description': description,
                    'data': {}
                }),
                status=status_code,
                content_type='application/json',
            )

        # Trả ra kết quả nếu thành công

        status_code = 200
        description = _l('Lấy tin nhắn thành công').__str__()
        app.logger.info(log_msg.format(
            status_code=status_code,
            description=description,
        ))
        data = []
        for mes in messages:
            data.append(mes.to_dict())
        return Response(
            json.dumps({
                'status': True,
                'status_code': 'S001',
                'description': description,
                'data': data
            }),
            status=status_code,
            content_type='application/json',
        )
