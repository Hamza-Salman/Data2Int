import json
from bson import json_util
import os
from flask import app, Flask, render_template, request
from pymongo import MongoClient
import pandas as pd
import numpy as np

from xmlUpload import xml_upload
from xlsxUpload import xlsx_upload
from csvUpload import csv_upload
from virusScanFile import virus_scan

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'donorschoose'


def upload(extension, filename, uploaded_file, upload_path, duplicatesInput, DB_HOST, DB_PORT, DB_Name) -> bool:
    print("Case 1: This file extension is " + extension)
    print(filename)

    uploaded_file.save(os.path.join(upload_path, filename))  # commented out + extension

    has_virus = virus_scan(uploaded_file, upload_path)

    # check the scan result
    if has_virus:
        # Check if the file exists at the specified directory first before deleting
        if os.path.exists(upload_path + "/" + filename):
            os.remove(upload_path + "/" + filename)
        return False

    if extension == ".xml":
        xml_upload(uploaded_file.filename, upload_path, duplicatesInput, DB_HOST, DB_PORT, DB_Name)
    # Convert file method goes here
    elif extension == ".csv":
        # json_data = convert_file(uploaded_file.filename, app.config["UPLOAD_FOLDER"])
        csv_upload(uploaded_file.filename, upload_path, duplicatesInput, DB_HOST, DB_PORT, DB_Name)
    elif extension == ".xlsx":
        # json_data = convert_file(uploaded_file.filename, app.config["UPLOAD_FOLDER"])
        # print(json_data)
        xlsx_upload(uploaded_file.filename, upload_path, duplicatesInput, DB_HOST, DB_PORT, DB_Name)

    return True
