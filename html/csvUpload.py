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

    if (duplicatesInput == "NoDupes"):
        #print(reader)
        no_dupes = []
        for each in reader:
            if each not in no_dupes:
                no_dupes.append(each)
                
        collection.insert_many(no_dupes)
    else:
        collection.insert_many(reader)
    
    connection.close();
