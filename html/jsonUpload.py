from pymongo import MongoClient, collection
import json

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
        
        for each in no_dupes:
            collection.insert(each)
    else:
        for i in json_data:
            collection.insert_one(i)

    connection.close()
