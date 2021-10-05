from pymongo import MongoClient, collection
import pandas as pd
import json
import csv
import sys, getopt, pprint


def xlsx_upload(uploaded_file, path_to_file, DB_HOST, DB_PORT, DB_Name):
    COLLECTION_NAME = uploaded_file.split('.')[0]

    connection = MongoClient(DB_HOST, DB_PORT)

    collection = connection[DB_Name][COLLECTION_NAME]

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

    no_dupes = []
    for each in reader:
        row = {}
        for field in list_of_columns[0]:
            row[field] = each[field]
            
        if row not in no_dupes:
            no_dupes.append(row)
            
    for each in no_dupes:
        collection.insert(each)