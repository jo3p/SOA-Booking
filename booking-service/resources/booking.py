import time
import random
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
        result = QueryDB.booking_details(bookingid)
        if len(result) == 0:
            return {"Message": "Booking not found."}, 200
        return result.to_dict(orient='records')[0], 200


class Refund(Resource):
    @staticmethod
    def put():
        bookingid = request.args.get('bookingid')
        result = QueryDB.start_refund(bookingid)
        # return message:
        return result, 200

    @staticmethod
    def get():
        refund = request.args.get('refundid')
        result = QueryDB.refund_status(refund)
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

        query_parameters = {"bookingid": bookingid, "accomodation": accomodation, "userid": userid,
                            "start_date": start_date, "end_date": end_date, "total_amount": total_amount}
        filled_sql_query = open('resources/insert_booking.sql', 'r').read().format(**query_parameters)
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
        filled_sql_query = open('resources/my_bookings.sql', 'r').read().format(**query_parameters)
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
        filled_sql_query = open('resources/booking_details.sql', 'r').read().format(**query_parameters)
        query_result = pd.read_sql(filled_sql_query, connection)
        connection.close()
        return query_result

    def start_refund(bookingid):
        connection = pyodbc.connect(
            'DRIVER={FreeTDS};'
            'SERVER=34.91.7.86;'
            'PORT=1433;'
            'DATABASE=IS-database;'
            'UID=SA;'
            'PWD=Innov@t1onS', autocommit=True)
        query_parameters = {"bookingid": bookingid}
        query1 = open('resources/booking_exist.sql', 'r').read().format(**query_parameters)
        query1result = pd.read_sql(query1, connection)
        if query1result.iat[0, 0] == 0:
            connection.close()
            return {"message": "Booking does not exist"}
        query2 = open('resources/booking_details.sql', 'r').read().format(**query_parameters)
        query2result = pd.read_sql(query2, connection)
        if query2result.iat[0,6]==1:
            return {"message" : "Booking has already been refunded"}
        # Update the booking table
        set_booking_refunded_query = open('resources/booking_set_refunded.sql', 'r').read().format(**query_parameters)
        cur = connection.cursor()
        cur.execute(set_booking_refunded_query)
        # create new entry in refund table
        query_parameters["refundid"] = str(bookingid + str(int(time.time())))
        query_parameters["amount"] = query2result.iat[0, 7]
        query_parameters["randomdays"] = random.randint(1, 7)
        add_entry_refund_query = open('resources/add_entry_refund_query.sql', 'r').read().format(**query_parameters)
        cur.execute(add_entry_refund_query)
        connection.commit()
        connection.close()
        return {"message": "Refund succesfully initiated and logged!"}

    def refund_status(refundid):
        connection = pyodbc.connect(
            'DRIVER={FreeTDS};'
            'SERVER=34.91.7.86;'
            'PORT=1433;'
            'DATABASE=IS-database;'
            'UID=SA;'
            'PWD=Innov@t1onS', autocommit=True)
        query_parameters = {"refundid": refundid}
        filled_sql_query = open('resources/refund_details.sql', 'r').read().format(**query_parameters)
        query_result = pd.read_sql(filled_sql_query, connection).to_dict(orient='records')
        connection.close()
        if len(query_result) == 0:
            return {"message": "RefundID not found"}
        return query_result[0]
