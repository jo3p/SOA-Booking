from flask import Flask
from flask_restful import Api

from resources.booking import Booking, MyBookings, BookingUser

app = Flask(__name__)
api = Api(app)

api.add_resource(Booking, '/booking/', methods=['POST'])
api.add_resource(MyBookings, '/booking/mybookings/<string:userid>', methods=['GET'])
api.add_resource(BookingUser, '/booking/<string:bookingid>', methods=['GET','DELETE'])

app.run(host='0.0.0.0', port=5000, debug=True)

