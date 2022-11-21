from db import db

class Message(db.Document):
    title = db.StringField(required=True)
    content = db.StringField(required=True)