import json
import os

from bson import json_util
from flask import Flask, render_template, request
from pymongo import MongoClient
from convertFile import convert_file
from jsonUpload import json_upload
from uploadInterfaceTwo import upload

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'csv'}

app.config["UPLOAD_FOLDER"] = "/var/www/data2int.com/html/templates/uploadedFiles"
app.config["MAX_FILE_SIZE"] = 10485760

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'donorschoose'
COLLECTION_NAME = 'projects'
FIELDS = {'school_state': True, 'resource_type': True, 'poverty_level': True, 'date_posted': True,
          'total_donations': True, '_id': False}


# def max_filesize(filesize):
#     if int(filesize) <= app.config["MAX_FILE_SIZE"]:
#         return true
#     else:
#         return false

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/Upload', methods=['POST'])
@app.route('/Upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':

        # if max_filesize(request.cookies.get("filesize")):
        #     return render_template('ErrorFileUpload.html')

        uploaded_file = request.files['file']

        # File name can not be null
        if uploaded_file.filename == "":
            return render_template('ErrorFileUpload.html')

        # Scan files here
        # Mark's part
        # Kevin's edit
        # Get the extension
        extension = os.path.splitext(uploaded_file.filename)[1]  # extension = '.txt'
        fileName = os.path.basename(uploaded_file.filename)

        # Sanitary check the file extension
        # If the file extension .csv or .xlsx or .xml
        # Case 1
        if extension == ".csv" or extension == ".xlsx" or extension == ".xml":
            upload(extension, fileName, uploaded_file, app.config["UPLOAD_FOLDER"])
        # If the file extension .json
        elif extension == ".json":
            print("Case 2: This file extension is " + extension)
            uploaded_file.save(os.path.join(app.config["UPLOAD_FOLDER"], fileName))
            with open(app.config["UPLOAD_FOLDER"] + "/" + fileName) as json_file:
                json_data = json.load(json_file)
            json_upload(json_data, fileName)
            # Json file upload
        # Everything else
        # Render error file upload page
        else:
            print("Case 3: This file extension is '" + extension + "'. File upload error")
            return render_template("ErrorFileUpload.html")

        return render_template('SuccessfulUpload.html')


@app.route('/ErrorFileUpload')
def error_file_upload():
    return render_template('ErrorFileUpload.html')


@app.route('/Upload')
def upload_file_page():
    return render_template('UploadPage.html')



@app.route('/SuccessfulUpload')
def success_file_upload():
    return render_template('SuccessfulUpload.html')

@app.route('/UploadDev', methods=['POST'])
def upload_file_dev():
    if request.method == 'POST':

        uploaded_file = request.files['file']

        if uploaded_file.filename == "":
            return render_template('ErrorFileUpload.html')

        uploaded_file.save(os.path.join(app.config["UPLOAD_FOLDER"], uploaded_file.filename))
        return render_template('SuccessfulUpload.html')

@app.route('/UploadDev')
def upload_file_page_dev():
    return render_template('UploadDevFiles.html')

@app.route('/AccessingData')
def AccessingData():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    json_collection = connection[DBS_NAME]["test"]
    testfile = open("/var/www/data2int.com/html/templates/uploadedFiles/Test.json")
    json_data = json.load(testfile)
    for i in json_data:
        json_collection.insert_one(i)
    testfile.close()
    connection.close()
    return render_template('AccessingData.html')


@app.route('/new')
def new():
    return render_template('new.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/map')
def map():
    return render_template('map.html')


@app.route('/MeetingMinutes')
def MeetingMinutes():
    return render_template('MeetingMinutes.html')


@app.route('/DocumentLibrary')
def DocumentLibrary():
    return render_template('DocumentLibrary.html')


@app.route('/Programmer1')
def Programmer1():
    return render_template('Programmer1.html')


@app.route('/Programmer2')
def Programmer2():
    return render_template('Programmer2.html')


@app.route('/Programmer3')
def Programmer3():
    return render_template('Programmer3.html')


@app.route('/Programmer4')
def Programmer4():
    return render_template('Programmer4.html')


@app.route('/Programmer5')
def Programmer5():
    return render_template('Programmer5.html')


@app.route('/DevEnv')
def DevEnv():
    return render_template('DevEnv.html')


@app.route('/MongoDB')
def MongoDB():
    return render_template('MongoDB.html')


@app.route('/Flask')
def Flask():
    return render_template('Flask.html')


@app.route('/D3')
def D3():
    return render_template('D3.html')

@app.route('/Dc')
def Dc():
    return render_template('Dc.html')

@app.route('/Folium')
def Folium():
    return render_template('Folium.html')

@app.route('/Prism')
def Prism():
    return render_template('Prism.html')

@app.route('/BigData')
def BigData():
    return render_template('BigData.html')

@app.route('/Paraquet')
def Paraquet():
    return render_template('Paraquet.html')

@app.route('/Clusters')
def Clusters():
    return render_template('Clusters.html')



@app.route('/UsefulResources')
def UsefulResources():
    return render_template('UsefulResources.html')


@app.route("/donorschoose/projects")
def donorschoose_projects():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_NAME]
    projects = collection.find(projection=FIELDS, limit=100000)
    json_projects = []
    for project in projects:
        json_projects.append(project)
    json_projects = json.dumps(json_projects, default=json_util.default)
    connection.close()
    return json_projects


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
