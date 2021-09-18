from pymongo import MongoClient, collection
import json

def json_upload(json_data, uploaded_file):
    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 27017
    DBS_NAME = 'donorschoose'
    COLLECTION_NAME = uploaded_file.split('.')[0]

    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)

    collection = connection[DBS_NAME][COLLECTION_NAME]

    if json_data == "":
        return ""

    print(json_data)
    for i in json_data:
        collection.insert_one(i)

    connection.close()