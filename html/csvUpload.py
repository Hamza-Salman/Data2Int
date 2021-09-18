from pymongo import MongoClient, collection
import json
import csv
import sys, getopt, pprint


def csv_upload(uploaded_file, path_to_file):
    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 27017
    DBS_NAME = 'donorschoose'
    COLLECTION_NAME = uploaded_file.split('.')[0]

    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)

    collection = connection[DBS_NAME][COLLECTION_NAME]
    csvFile = open(path_to_file + "/" + uploaded_file, 'r')
    reader = csv.DictReader(csvFile)
    with open(path_to_file + "/" + uploaded_file) as csv_file:
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
        # print(row)