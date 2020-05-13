from flask_restful import Resource, reqparse
from flask import request
import pyodbc
import pandas as pd

'''
Only works for post request with json body similar to:
{
  "accomodations": "(3,5,1,4,2)",
  "prices": "(60,100,100,120,200)",
  "review_scores": "(5.6, 9.0, 5.1, 8.5, 7.9)"
}
'''


class QueryDisplay(Resource):
    def get(self):
        accomodations = request.args.get('accomodations')
        prices = request.args.get('prices')
        review_scores = request.args.get('review_scores')
        query = QueryDB.retrieve_query(accomodations)
        result = MergeQueries.merge(query,
                                    accomodations,
                                    prices,
                                    review_scores).to_dict(orient='records')

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
        filled_sql_query = open('resources/query_display.sql', 'r').read().format(**query_parameters)
        query_result = pd.read_sql(filled_sql_query, connection)
        connection.close()
        return query_result

class MergeQueries:
    def merge(query_results, accomodations, prices, review_scores):
        accomodations = accomodations.replace("(", "").replace(")", "")
        accomodations = list(tuple(map(int, accomodations.split(','))))
        prices = prices.replace("(", "").replace(")", "")
        prices = list(tuple(map(int, prices.split(','))))
        review_scores = review_scores.replace("(", "").replace(")", "")
        review_scores = list(tuple(map(float, review_scores.split(','))))
        ranked_db = pd.DataFrame(list(zip(accomodations, prices, review_scores)), columns=['accomodations', 'prices', 'review_scores'])
        ranked_db = ranked_db.merge(query_results, how='left', left_on="accomodations",
                                    right_on='accomodation_id')
        ranked_db.drop(['accomodations', 'accomodation_id'], axis=1, inplace=True)
        # Rearange the order
        ranked_db = ranked_db[['name', 'city', 'country', 'prices', 'review_scores']]
        ranked_db.columns = ['Name', 'City', 'Country', 'Price p.p', 'Review Score']
        del accomodations
        del prices
        del review_scores
        return ranked_db