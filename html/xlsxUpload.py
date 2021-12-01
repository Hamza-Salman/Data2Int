from pymongo import MongoClient, collection
import pandas as pd
import json
import csv
import sys, getopt, pprint
import random

from calcDeleteTime import seconds_until_end_of_day


def xlsx_upload(uploaded_file, path_to_file, duplicatesInput, DB_HOST, DB_PORT, DB_Name):
    COLLECTION_NAME = uploaded_file.split('.')[0]

    connection = MongoClient(DB_HOST, DB_PORT)

    collection = connection[DB_Name][COLLECTION_NAME]

    index_num = random.randint(0, 10000)
    index_name = "expire_date_time_" + str(index_num)

    print(index_name)

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

        collection.create_index(index_name, expireAfterSeconds=seconds_until_end_of_day())
        collection.insert_many(no_dupes)
    else:
        collection.create_index(index_name, expireAfterSeconds=seconds_until_end_of_day())
        collection.insert_many(reader)

    connection.close()
