from flask_restful import Resource, reqparse
from flask import request
import pyodbc
import pandas as pd

'''
Only works for post request with json body similar to:

{
	"accomodations" : "(1,2)"
}
'''


class Ranks(Resource):
    def get(self):
        r = request.get_json(force=True)
        result = QueryDB.retrieve_query(r["accomodations"]).to_dict(orient='records')
        return result, 200


class QueryDB:
    def retrieve_query(accomodations):

        connection = pyodbc.connect(
            'DRIVER={FreeTDS};'
            'SERVER=34.91.7.86;'
            'PORT=1433;'
            'DATABASE=IS-database;'
            'UID=SA;'
            'PWD=Innov@t1onS', autocommit=True)

        query_parameters = {
            "accomodations": accomodations
        }

        filled_sql_query = open('resources/ranking.sql', 'r').read().format(**query_parameters)
        query_result = pd.read_sql(filled_sql_query, connection)

        connection.close()

        return query_result
