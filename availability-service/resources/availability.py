from flask_restful import Resource, reqparse
from flask import request
import pyodbc
import pandas as pd
from datetime import datetime

'''
Only works for post request with json body similar to:

{
	"start_date" : "2020-06-01",
	"end_date" : "2020-06-04",
	"city" : "Amsterdam",
	"country" : "The Netherlands",
	"n_persons" : 3
}
'''

class AvailableAccomodations(Resource):
    def post(self):
        r = request.get_json(force=True)
        result = QueryDB.retrieve_query(r["start_date"],
                                        r["end_date"],
                                        r["city"],
                                        r["country"],
                                        r["n_persons"]).to_dict(orient='records')
        return result, 200

class AllAccomodations(Resource):
    def get(self):
        result = QueryDB.retrieve_all().to_dict(orient='records')
        return result

class QueryDB:
    def retrieve_query(start_date, end_date, city, country, n_persons):
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
        length_stay = (end_date_obj - start_date_obj).days + 1

        connection = pyodbc.connect(
            'DRIVER={FreeTDS};'
            'SERVER=34.91.7.86;'
            'PORT=1433;'
            'DATABASE=IS-database;'
            'UID=SA;'
            'PWD=Innov@t1onS', autocommit=True)

        query_parameters = {
            "start_date": start_date,
            "end_date": end_date,
            "city": city,
            "country": country,
            "n_persons": n_persons,
            "length_stay": length_stay
        }

        filled_sql_query = open('resources/availability.sql', 'r').read().format(**query_parameters)
        query_result = pd.read_sql(filled_sql_query, connection)
        connection.close()

        return query_result

    def retrieve_all():
        connection = pyodbc.connect(
            'DRIVER={FreeTDS};'
            'SERVER=34.91.7.86;'
            'PORT=1433;'
            'DATABASE=IS-database;'
            'UID=SA;'
            'PWD=Innov@t1onS', autocommit=True)

        filled_sql_query = open('resources/allavailability.sql', 'r').read()
        query_result = pd.read_sql(filled_sql_query, connection)
        connection.close()

        return query_result

