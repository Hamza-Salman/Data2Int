from pymongo import MongoClient


def clean_database(uploaded_file, DB_HOST, DB_PORT, DB_Name):
    COLLECTION_NAME = uploaded_file.split('.')[0]
    # print(COLLECTION_NAME)

    connection = MongoClient(DB_HOST, DB_PORT)

    collection = connection[DB_Name][COLLECTION_NAME]

    if collection.count() > 0:
        print("dropping")
        collection.drop()

    connection.close()
