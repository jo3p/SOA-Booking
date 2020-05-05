import pyodbc
import pandas as pd

print("Connecting to database")
conn = pyodbc.connect(
    'DRIVER={FreeTDS};'
    'SERVER=34.91.7.86;'
    'PORT=1433;'
    'DATABASE=IS-database;'
    'UID=SA;'
    'PWD=Innov@t1onS', autocommit=True)
print("Connected to Database")

# print("Creating new Database")
# cur = conn.cursor()
# cur.execute("CREATE DATABASE [Availability]")
# print("Database Availability created")
# cur.close()
# conn.close()
#
# print("Connecting to Availability Database")
# conn = pyodbc.connect(
#     'DRIVER={FreeTDS};'
#     'SERVER=db;'
#     'PORT=1433;'
#     'DATABASE=Availability;'
#     'UID=SA;'
#     'PWD=Innov@t1onS', autocommit=True)
# print("Connected to availability")

# cur = conn.cursor()
# cur.execute("CREATE TABLE Availability(Date date, Accomodation_ID int, Accomodation_name varchar(30), City varchar(30), "
#             "Country varchar(30),Availability int)")
# conn.commit()
# print("Database Availability created")
#
# cur.execute(f"INSERT INTO [Availability] ([Date],[Accomodation_ID],[Accomodation_name],[City],[Country],"
#             f"[Availability]) VALUES ('2020-05-18', 1,'Amstel Hotel','Amsterdam','The Netherlands',1)")
# conn.commit()

cur = conn.cursor()
df = pd.DataFrame(cur.execute('SELECT * FROM [Availability]'))
print(df)
