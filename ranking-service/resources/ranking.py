from flask_restful import Resource, reqparse
from flask import request
import pyodbc
import pandas as pd


class Ranks(Resource):
    def get(self):
        accomodations = request.args.get('accomodations')
        prices = request.args.get('prices')
        query = QueryDB.retrieve_query(accomodations)
        result = RankAccomodations.ranking(query, prices)
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
        query_parameters = {"accomodations": accomodations}
        filled_sql_query = open('resources/ranking.sql', 'r').read().format(**query_parameters)
        query_result = pd.read_sql(filled_sql_query, connection)
        connection.close()
        return query_result


class RankAccomodations:
    def ranking(query_results, prices):
        prices = prices.replace("(", "").replace(")", "")
        prices = list(tuple(map(int, prices.split(','))))
        query_results['prices'] = prices
        query_results = query_results.sort_values(["prices", "commission_paid", "review_score", "amount_of_bookings"],
                                                  ascending = (True, False, False, False))
        return_query = {"accomodations": str(tuple(query_results["accomodation_id"].to_list())).replace(" ", ""),
                        "prices": str(tuple(query_results["prices"].to_list())).replace(" ", ""),
                        "review_scores": str(tuple(query_results['review_score'].to_list())).replace(" ", "")}
        return return_query
