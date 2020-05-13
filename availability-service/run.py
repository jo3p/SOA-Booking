from flask import Flask
from flask_restful import Api
from resources.availability import AvailableAccomodations, AllAccomodations

app = Flask(__name__)
api = Api(app)
api.add_resource(AvailableAccomodations, '/', methods=['GET'])
api.add_resource(AllAccomodations, '/all/', methods=['GET'])
app.run(host='0.0.0.0', port=5000, debug=True)
