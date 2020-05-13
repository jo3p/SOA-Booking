from flask import Flask
from flask_restful import Api
from resources.query_display import QueryDisplay

app = Flask(__name__)
api = Api(app)
api.add_resource(QueryDisplay, '/', methods=['GET'])
app.run(host='0.0.0.0', port=5000, debug=True)
