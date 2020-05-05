import requests


def get_booking(id):
    url = 'http://localhost:5000/placed_bookings/'
    httprequest = requests.get(url + str(id))
    return httprequest.json()

print(get_booking(2))
