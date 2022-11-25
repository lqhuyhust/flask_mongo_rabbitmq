from flask_restful import Api

from api import create_app
from api.resources.message import SendMessage
from api.resources.index import Index, DocsApi

# KHỞI TẠO APP
app = create_app()

# KHAI BÁO ROUTE
API = Api(app)

# Docs API
API.add_resource(Index, '/', endpoint='index')
API.add_resource(DocsApi, '/docs', endpoint='docsapi')

# Message API
API.add_resource(SendMessage, '/messages', endpoint='send_message')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
