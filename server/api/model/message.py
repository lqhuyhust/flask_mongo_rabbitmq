import json
from api import db


class Message(db.Document):
    title = db.StringField(required=True)
    content = db.StringField(required=True)

    def to_dict(self):
        result = json.loads(self.to_json())
        result["_id"] = str(self.id)
        return result
