import pandas as pd
import pyodbc
from flask import request
from flask_restful import Resource


class Price(Resource):
    @staticmethod
    def get():
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        accomodations = request.args.get('accomodations')
        result = QueryDB.retrieve_query(start_date, end_date, accomodations)
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
        query_parameters = {"start_date": start_date, "end_date": end_date, "accomodations_string": accomodations_string}
        filled_sql_query = open('resources/price.sql', 'r').read().format(**query_parameters)
        query_result = pd.read_sql(filled_sql_query, connection)
        result = {'accomodations': str(tuple(query_result['accomodation_id'].to_list())).replace(" ", ""),
                  'prices': str(tuple(query_result['total_price'].to_list())).replace(" ", "")}
        connection.close()
        return result
