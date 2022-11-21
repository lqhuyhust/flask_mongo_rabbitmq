from flask_restful import Resource
from common.send_message import send_message
from model.message import Message
from flask import jsonify, request

class SendMessage(Resource):
    def post(self):
        title = request.form.get('title')
        content = request.form.get('content')
        message = Message(
            title = title,
            content = content,
        )
        message.save()
        send_message(content)
        return "OK"
    
    def get(request):
        messages = Message.objects()
        return jsonify(messages)