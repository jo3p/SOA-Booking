from flask import Flask
from flask_restful import Api
from flask_restful import Resource, reqparse
from flask import request
import pandas as pd

hotellist = [['1', 'Kurhaus', True],
             ['2', 'Van der Valk Hotel Tilburg', False]]

hotels = pd.DataFrame(hotellist, columns=['id', 'hotel_name', 'availability'])



