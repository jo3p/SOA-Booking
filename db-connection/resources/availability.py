from flask_restful import Resource, reqparse
from flask import request
import pyodbc
import pandas as pd
from datetime import datetime
import json

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
        result = QueryDB.retrieve_query(r["start_date"],r["end_date"],r["city"],r["country"],r["n_persons"]).to_dict(orient='records')
        return result, 201  # 201 Created HTTP status code

class QueryDB():

    def retrieve_query(start_date, end_date, city, country, n_persons):
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
        length_stay = (end_date_obj - start_date_obj).days + 1

        conn = pyodbc.connect(
            'DRIVER={FreeTDS};'
            'SERVER=34.91.7.86;'
            'PORT=1433;'
            'DATABASE=IS-database;'
            'UID=SA;'
            'PWD=Innov@t1onS', autocommit=True)

        sql_query = f"SELECT * " \
                    f"FROM Accomodations " \
                    f"WHERE city = '{city}' AND country = '{country}' AND accomodation_id IN (" \
                    f"SELECT accomodation_id " \
                    f"FROM Availability " \
                    f"WHERE capacity >= {n_persons} AND date BETWEEN '{start_date}' AND '{end_date}' " \
                    f"GROUP BY accomodation_id " \
                    f"HAVING COUNT(accomodation_id) = {length_stay});"

        query_result = pd.read_sql(sql_query, conn)
        conn.close()

        return query_result


