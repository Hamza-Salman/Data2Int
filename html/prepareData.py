import pandas as pd
from pymongo import MongoClient

# Global variables
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DB_NAME = 'donorschoose'


def fetchData(filename, DB_HOST, DB_PORT, DB_Name):
    connection = MongoClient(DB_HOST, DB_PORT)

    collection = connection[DB_Name][filename]
    cursor = collection.find({}, {'_id': False})
    connection.close()
    return pd.DataFrame(cursor)


def getColumnsName(data):
    return data.columns.values


def getPreviewData(data):
    return data.head()
