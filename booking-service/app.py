from flask import Flask
from flask_restful import Api
from flask_restful import Resource, reqparse
from flask import request

# dummy data
placedBookings = [
    {
        "booking_id": 1,
        "hotel_id": 654772,
        "hotel_name": "Grand Hotel Amrâth Kurhaus",
        "address": {
            "postcode": "5038 XH",
            "street": "Gevers Deynootplein",
            "houseNo": 30,
            "city": "Den Haag"
        }
    }
]


class PlacedBookings(Resource):

    def get(self, booking_id):
        for booking in placedBookings:
            if booking_id == booking['booking_id']:
                return booking, 200
        return {'message': 'Booking not found'}, 404

    def put(self, booking_id):  # TODO: Uitzoeken wat dit precies doet en aanpassen
        parser = reqparse.RequestParser()
        parser.add_argument('rating', type=int, help='Rate to charge for this resource')
        args = parser.parse_args(strict=True)

        for booking in placedBookings:
            if booking_id == booking['booking_id']:
                booking['rating'] = args['rating']
                return booking, 200

    def delete(self, booking_id):
        booking_to_be_deleted = None
        for booking in placedBookings:
            if booking_id == booking['booking_id']:
                booking_to_be_deleted = booking
                break

        if booking_to_be_deleted:
            placedBookings.remove(booking_to_be_deleted)
            return '{} is deleted.'.format(booking), 200
        return {'message': 'Booking to delete not found'}, 404


class PlaceBooking(Resource):

    def post(self):
        booking_to_be_added = request.get_json(force=True)
        booking_id = booking_to_be_added['booking_id']
        for booking in placedBookings:
            if booking_id == booking['booking_id']:
                return {'message': 'Record with booking_id {} already exists.'.format(booking_id)}, 500
        placedBookings.append(booking_to_be_added)
        return booking_to_be_added, 201



app = Flask(__name__)
api = Api(app)

api.add_resource(PlaceBooking, '/place_booking/', methods=['POST'])
api.add_resource(PlacedBookings, '/placed_bookings/<int:booking_id>', methods=['GET', 'PUT', 'DELETE'])

app.run(host='0.0.0.0', port=5000, debug=True)
