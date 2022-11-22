from flask_restful import Resource
from common.send_message import send_message
from model.message import Message
from flask import jsonify, request
from common.validate import message_validate
from flask import current_app as app

class SendMessage(Resource):
    def post(self):
        errors = message_validate.validate(request.form)
        if errors:
            return str(errors)
        title = request.form.get('title')
        content = request.form.get('content')
        message = Message(
            title = title,
            content = content,
        )
        message.save()
        send_message(content)
        app.logger.info('Message title: %s', title)
        app.logger.info('Message content: %s', content)
        return "OK"
    
    def get(request):
        messages = Message.objects()
        return jsonify(messages)