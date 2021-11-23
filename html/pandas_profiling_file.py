import numpy as np
import pandas as pd
from pandas_profiling import ProfileReport
import csv
import pandas as pd
from pymongo import MongoClient


def pandas_profile(uploaded_file, path_to_file, DB_HOST, DB_PORT, DB_Name):
    print(uploaded_file)
    print(path_to_file)
    csvFile = open(path_to_file + "/" + uploaded_file, 'r')
    reader = csv.DictReader(csvFile)
    with open(path_to_file + "/" + uploaded_file) as csv_file:
        csvReader = csv.reader(csv_file, delimiter=',')
        list_of_columns = []
        # get list of columns
        for row in csvReader:
            list_of_columns = row
            break

        # open connection
        COLLECTION_NAME = uploaded_file.split('.')[0]
        connection = MongoClient(DB_HOST, DB_PORT)
        collection = connection[DB_Name][COLLECTION_NAME]

        profile = ProfileReport(reader, title="Pandas Profiling Report", explorative=True)
