import pyodbc
import pandas as pd
from datetime import datetime


start_date = '2020-06-01'
end_date = '2020-06-04'
city = 'Amsterdam'
country = 'The Netherlands'
n_persons = 3

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

print(query_result)
