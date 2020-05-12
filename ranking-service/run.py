from flask import Flask
from flask_restful import Api

from resources.ranking import Ranks

app = Flask(__name__)
api = Api(app)

api.add_resource(Ranks, '/ranking/', methods=['GET'])

app.run(host='0.0.0.0', port=5000, debug=True)

