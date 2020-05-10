from flask_restful import Resource, reqparse
from flask import request
import pyodbc
import pandas as pd

'''
Only works for post request with json body similar to:

{
   "start_date" : "2020-06-01",
	"end_date" : "2020-06-04",
	"accomodation_id" : "(1,2)"
}
'''


class Price(Resource):
    def post(self):
        r = request.get_json(force=True)

        result = QueryDB.retrieve_query(r["start_date"],
                                        r["end_date"],
                                        r["accomodations"]).to_dict(orient='records')
        return result, 200


class QueryDB:
    def retrieve_query(start_date, end_date, accomodations_string):

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
            "accomodations_string": accomodations_string
        }

        filled_sql_query = open('resources/price.sql', 'r').read().format(**query_parameters)
        query_result = pd.read_sql(filled_sql_query, connection)
        connection.close()

        return query_result
