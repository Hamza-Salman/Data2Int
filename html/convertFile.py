import os
import xmltodict
import json
import pandas as pd


def convert_file(uploaded_file, path_to_file):
    # Get the extension
    ext = os.path.splitext(uploaded_file)[1]

    # Defensive programming
    if ext != ".xml" and ext != ".csv" and ext != ".xml":
        return ""

    if ext == ".xml":
        with open(path_to_file + "/data2int_file.xml") as xml_file:  # Open targeted file
            data_dict = xmltodict.parse(xml_file.read())  # Load XML data into dictionary datatype
            xml_file.close()  # Close XML file to reduce the risk of being unwarranted modified or read.
            json_data = json.dumps(data_dict)  # json.dumps() take a json object and returns a string
            print(json_data)

    elif ext == ".csv":
        df = pd.read_csv("r'" + path_to_file + "/data2int_file.csv'")  # Read CSV file
        json_data = df.to_json()  # Write output in JSON file

    # This file extension has only been tested for an excel file with only ONE tab
    elif ext == ".xlsx":
        excel_data_df = pd.read_excel(path_to_file + "/data2int_file.xlsx")
        json_data = excel_data_df.to_json()

    return json_data

# def scanning() -> bool:
# def jsonImport() -> bool:
# def xmlImport() -> bool:
# def csvImport() -> bool:  # This will most likely also include xlsx because csv and xlsx is the same
