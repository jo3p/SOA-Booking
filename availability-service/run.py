from flask import Flask
from flask_restful import Api

from resources.availability import AvailableAccomodations, AllAccomodations

app = Flask(__name__)
api = Api(app)

api.add_resource(AvailableAccomodations, '/availability/accomodations/', methods=['GET'])
api.add_resource(AllAccomodations, '/availability/allaccomodations/', methods=['GET'])

app.run(host='0.0.0.0', port=5000, debug=True)
#app.run(port=81, debug=True)

# In the context of servers, 0.0.0.0 can mean "all IPv4 addresses on the local machine".
