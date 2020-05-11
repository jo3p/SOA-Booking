from flask import Flask
from flask_restful import Api

from resources.price import Price

app = Flask(__name__)
api = Api(app)

api.add_resource(Price, '/price/<string:start_date>/<string:end_date>/<string:accomodations>', methods=['GET'])

app.run(host='0.0.0.0', port=5000, debug=True)
