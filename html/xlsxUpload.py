from pymongo import MongoClient, collection
import pandas as pd
import json
import csv
import sys, getopt, pprint

from calcDeleteTime import seconds_until_end_of_day


def xlsx_upload(uploaded_file, path_to_file, duplicatesInput, DB_HOST, DB_PORT, DB_Name):
    COLLECTION_NAME = uploaded_file.split('.')[0]

    connection = MongoClient(DB_HOST, DB_PORT)

    collection = connection[DB_Name][COLLECTION_NAME]

    excel_file = pd.read_excel(path_to_file + "/" + uploaded_file, engine='openpyxl', index_col=None)

    excel_file.to_csv(path_to_file + "/" + COLLECTION_NAME + ".csv", encoding='utf-8', index=False)

    csvFile = open(path_to_file + "/" + COLLECTION_NAME + ".csv", 'r')
    reader = csv.DictReader(csvFile)

    if duplicatesInput == "NoDupes":
        # print(reader)
        no_dupes = []
        for each in reader:
            if each not in no_dupes:
                no_dupes.append(each)

        print(seconds_until_end_of_day().seconds)

        collection.create_index("expire_date_time", expireAfterSeconds=seconds_until_end_of_day().seconds)
        collection.insert_many(no_dupes)
    else:
        collection.create_index("expire_date_time", expireAfterSeconds=seconds_until_end_of_day().seconds)
        collection.insert_many(reader)

    connection.close()
