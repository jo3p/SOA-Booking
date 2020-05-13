import time

import pandas as pd
import pyodbc
from flask import request
from flask_restful import Resource


class PlaceBooking(Resource):
    @staticmethod
    def post():
        r = request.get_json(force=True)
        QueryDB.insert_booking(r["accomodation"],
                               r["userid"],
                               r["start_date"],
                               r["end_date"],
                               r["total_amount"])

        return {"message": "Successful booking!"}, 200  # TODO: check if booking exists


class MyBookings(Resource):
    @staticmethod
    def get():
        userid = request.args.get('userid')
        result = QueryDB.my_bookings(userid).to_dict(orient='records')
        return result, 200


class BookingDetails(Resource):
    @staticmethod
    def get():
        bookingid = request.args.get('bookingid')
        result = QueryDB.booking_details(bookingid).to_dict(orient='records')
        return result, 200


class QueryDB:

    def insert_booking(accomodation, userid, start_date, end_date, total_amount):
        bookingid = str(str(userid) + str(int(time.time())))
        time.sleep(1)

        connection = pyodbc.connect(
            'DRIVER={FreeTDS};'
            'SERVER=34.91.7.86;'
            'PORT=1433;'
            'DATABASE=IS-database;'
            'UID=SA;'
            'PWD=Innov@t1onS', autocommit=True)

        query_parameters = {
            "bookingid": bookingid,
            "accomodation": accomodation,
            "userid": userid,
            "start_date": start_date,
            "end_date": end_date,
            "total_amount": total_amount
        }

        filled_sql_query = open('resources/booking.sql', 'r').read().format(**query_parameters)

        cur = connection.cursor()
        cur.execute(filled_sql_query)
        connection.commit()
        connection.close()

    def my_bookings(userid):
        connection = pyodbc.connect(
            'DRIVER={FreeTDS};'
            'SERVER=34.91.7.86;'
            'PORT=1433;'
            'DATABASE=IS-database;'
            'UID=SA;'
            'PWD=Innov@t1onS', autocommit=True)

        query_parameters = {"userid": userid}

        filled_sql_query = open('resources/booking2.sql', 'r').read().format(**query_parameters)
        query_result = pd.read_sql(filled_sql_query, connection)
        connection.close()

        return query_result

    def booking_details(bookingid):
        connection = pyodbc.connect(
            'DRIVER={FreeTDS};'
            'SERVER=34.91.7.86;'
            'PORT=1433;'
            'DATABASE=IS-database;'
            'UID=SA;'
            'PWD=Innov@t1onS', autocommit=True)

        query_parameters = {"bookingid": bookingid}

        filled_sql_query = open('resources/booking3.sql', 'r').read().format(**query_parameters)
        query_result = pd.read_sql(filled_sql_query, connection)
        connection.close()

        return query_result

    def booking_deletion(bookingid):
        connection = pyodbc.connect(
            'DRIVER={FreeTDS};'
            'SERVER=34.91.7.86;'
            'PORT=1433;'
            'DATABASE=IS-database;'
            'UID=SA;'
            'PWD=Innov@t1onS', autocommit=True)

        query_parameters = {"bookingid": bookingid}

        filled_sql_query = open('resources/booking4.sql', 'r').read().format(**query_parameters)

        cur = connection.cursor()
        cur.execute(filled_sql_query)
        connection.commit()
        connection.close()
