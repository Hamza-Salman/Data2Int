from pymongo import MongoClient, collection
import json

from calcDeleteTime import seconds_until_end_of_day


def json_upload(json_data, uploaded_file, duplicatesInput, DB_HOST, DB_PORT, DB_Name):
    COLLECTION_NAME = uploaded_file.split('.')[0]

    connection = MongoClient(DB_HOST, DB_PORT)

    collection = connection[DB_Name][COLLECTION_NAME]

    if json_data == "":
        return ""


    if (duplicatesInput == "NoDupes"):
        no_dupes = []
        #print(json_data)
        for i in json_data:
            if i not in no_dupes:
                no_dupes.append(i)

        collection.create_index("expire_date_time", expireAfterSeconds=seconds_until_end_of_day().seconds)
        collection.insert_many(no_dupes)
    else:
        collection.create_index("expire_date_time", expireAfterSeconds=seconds_until_end_of_day().seconds)
        collection.insert_many(json_data)

    connection.close()
