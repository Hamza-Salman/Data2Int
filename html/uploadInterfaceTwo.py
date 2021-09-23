import json
from bson import json_util
import os
from flask import app, Flask, render_template, request
from pymongo import MongoClient

from xmlUpload import xml_upload
from xlsxUpload import xlsx_upload
from csvUpload import csv_upload
from virusScanFile import virus_scan

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'donorschoose'


def upload(extension, fileName, uploaded_file, uploadPath) -> bool:
    print("Case 1: This file extension is " + extension)
    print(fileName)

    uploaded_file.save(os.path.join(uploadPath, fileName))  # commented out + extension

    has_virus = virus_scan(uploaded_file, uploadPath)  # grabs result of virus scan api

    # Check result for virus
    if has_virus:
        # Check if the file exists at the specified directory first before deleting
        if os.path.exists(uploadPath + "/" + fileName):
            os.remove(uploadPath + "/" + fileName)
            return False

    else:
        print("File is clean")

    if extension == ".xml":
        xml_upload(uploaded_file.filename, uploadPath)
    # Convert file method goes here
    elif extension == ".csv":
        # json_data = convert_file(uploaded_file.filename, app.config["UPLOAD_FOLDER"])
        csv_upload(uploaded_file.filename, uploadPath)
    elif extension == ".xlsx":
        # json_data = convert_file(uploaded_file.filename, app.config["UPLOAD_FOLDER"])
        # print(json_data)
        xlsx_upload(uploaded_file.filename, uploadPath)

    return True

