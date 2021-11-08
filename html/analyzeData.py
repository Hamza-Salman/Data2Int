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
            #print("\n")
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
                    #print(each)
                    float(each)
                    #print("Measure")
                except:
                    is_measure = False
                    #print(each)
                    #print("Dimension")
                    analyzed_columns[col] = "dimension"
                    break
            if is_measure:
                analyzed_columns[col] = "measure"
        
        print("\n")
        
        largest_average = 0
        largest_average_variable = ""
        for analyzed in analyzed_columns.items():
            current_average = 0
            counter = 0
            if(analyzed[1] == "measure" and analyzed[0] != "ID"):
                FIELD = {analyzed[0] : True, "_id" : False}
                vals = collection.find(projection = FIELD)
                for i in vals:
                    for j in i.values():
                        current_average += float(j)
                        counter += 1
                current_average /= counter
            if (current_average > largest_average):
                largest_average = current_average
                largest_average_variable = analyzed[0]
            
        analyzed_columns[largest_average_variable] = "largestMeasure"
        connection.close()
        return analyzed_columns