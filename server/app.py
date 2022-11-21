from flask import Flask
from flask_restful import Api
from db import db

app = Flask(__name__)
api = Api(app)


app.config["MONGODB_SETTINGS"] = [
    {
        "db": "message_db",
        "host": "mongodb",
        "port": 27017,
    }   
]
db.init_app(app)

from resources.message import SendMessage
api.add_resource(SendMessage, '/messages')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

