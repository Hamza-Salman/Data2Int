from os import dup
from pymongo import MongoClient, collection
import json
import csv
import sys, getopt, pprint


def csv_upload(uploaded_file, path_to_file, duplicatesInput, DB_HOST, DB_PORT, DB_Name):
    COLLECTION_NAME = uploaded_file.split('.')[0]

    connection = MongoClient(DB_HOST, DB_PORT)

    collection = connection[DB_Name][COLLECTION_NAME]
    csvFile = open(path_to_file + "/" + uploaded_file, 'r')
    reader = csv.DictReader(csvFile)
    with open(path_to_file + "/" + uploaded_file) as csv_file:
        csvReader = csv.reader(csv_file, delimiter=',')
        list_of_columns = []
        for row in csvReader:
            list_of_columns.append(row)
            break

    if (duplicatesInput == "NoDupes"):
        #print(reader)
        no_dupes = []
        for each in reader:
            row = {}
            for field in list_of_columns[0]:
                row[field] = each[field]
                
            if row not in no_dupes:
                no_dupes.append(row)
                
        for each in no_dupes:
            collection.insert(each)
    else:
        for each in reader:
            row={}
            for field in list_of_columns[0]:
                row[field]=each[field]
            collection.insert(row)
            #print(row)