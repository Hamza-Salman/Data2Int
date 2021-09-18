from pymongo import MongoClient, collection
import pandas as pd
import json
import csv
import sys, getopt, pprint


def xlsx_upload(uploaded_file, path_to_file):
    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 27017
    DBS_NAME = 'donorschoose'
    COLLECTION_NAME = uploaded_file.split('.')[0]

    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)

    collection = connection[DBS_NAME][COLLECTION_NAME]

    excel_file = pd.read_excel(path_to_file + "/" + uploaded_file, engine='openpyxl', index_col=None)

    excel_file.to_csv(path_to_file + "/" + COLLECTION_NAME + ".csv", encoding='utf-8', index=False)

    csvFile = open(path_to_file + "/" + COLLECTION_NAME + ".csv", 'r')
    reader = csv.DictReader(csvFile)
    with open(path_to_file + "/" + COLLECTION_NAME + ".csv") as csv_file:
        csvReader = csv.reader(csv_file, delimiter=',')
        list_of_columns = []
        for row in csvReader:
            list_of_columns.append(row)
            break

    for each in reader:
        row = {}
        for field in list_of_columns[0]:
            row[field] = each[field]
        collection.insert(row)