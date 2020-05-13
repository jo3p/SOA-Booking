from flask import Flask
from flask_restful import Api

from resources.booking import PlaceBooking, MyBookings, BookingDetails, Refund

app = Flask(__name__)
api = Api(app)

api.add_resource(PlaceBooking, '/place_booking/', methods=['POST'])
api.add_resource(MyBookings, '/my_bookings/', methods=['GET'])
api.add_resource(BookingDetails, '/booking_details/', methods=['GET'])
api.add_resource(Refund, '/start_refund/', methods=['PUT', 'GET'])


app.run(host='0.0.0.0', port=5000, debug=True)

