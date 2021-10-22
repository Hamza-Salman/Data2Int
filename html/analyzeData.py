import csv
from numpy import equal
import pandas as pd
from collections import OrderedDict, Counter
from pymongo import MongoClient

def analyze_data(uploaded_file, path_to_file, DB_HOST, DB_PORT, DB_Name):
    print(uploaded_file)
    print(path_to_file)
    csvFile = open(path_to_file + "/" + uploaded_file, 'r')
    reader = csv.DictReader(csvFile)
    with open(path_to_file + "/" + uploaded_file) as csv_file:
        csvReader = csv.reader(csv_file, delimiter=',')
        list_of_columns = []
        #get list of columns 
        for row in csvReader:
            list_of_columns = row
            break

        #open connection
        COLLECTION_NAME = uploaded_file.split('.')[0]
        connection = MongoClient(DB_HOST, DB_PORT)
        collection = connection[DB_Name][COLLECTION_NAME]

        
        analyzed_columns = {}
        for col in list_of_columns:
            print("\n")
            FIELDS = {col: True}
            testCol = collection.find(projection=FIELDS)

            #isolate values from database for analysis
            column = []
            is_measure = True
            for i in testCol:
                row = []
                for value in i.values():
                    row.append(value)
                column.append(row[-1])
            for each in column:
                try:
                    print(each)
                    float(each)
                    print("Measure")
                except:
                    is_measure = False
                    print(each)
                    print("Dimension")
                    analyzed_columns[col] = "dimension"
                    break
            if is_measure:
                analyzed_columns[col] = "measure"
        
        print("\n")
        for analyzed in analyzed_columns.items():
            print(analyzed)