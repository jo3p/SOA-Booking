from flask import Flask
from flask_restful import Api
from resources.place_booking import PlaceBooking, PlaceBookings

app = Flask(__name__)
api = Api(app)

api.add_resource(PlaceBookings, '/place_booking/', methods=['POST'])
api.add_resource(PlaceBooking, '/placed_bookings/<int:booking_id>', methods=['GET', 'PUT', 'DELETE'])

app.run(host='0.0.0.0', port=5001, debug=True)