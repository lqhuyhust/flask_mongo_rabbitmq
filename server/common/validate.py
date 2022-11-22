from marshmallow import Schema, fields, validates, ValidationError 

class CreateMessage(Schema):
    title = fields.Str()
    content = fields.Str()

    @validates("title")
    @validates("content")
    def empty_text_error(self, value):
        if len(value) == 0:
            raise ValidationError("This field can not be empty")

    @validates("title")
    def length_title(self, value):
        if len(value) > 20:
            raise ValidationError("Title is no longer than 20 characters")

    @validates("content")
    def length_content(self, value):
        if len(value) > 50:
            raise ValidationError("Content is no longer than 50 characters")

message_validate = CreateMessage()
