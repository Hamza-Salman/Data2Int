import json
import os

from bson import json_util
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from prepareData import getPreviewData
from prepareData import fetchData, getColumnsName
from jsonUpload import json_upload
from uploadData import upload
from virusScanFile import virus_scan
from cleanDatabase import clean_database
from analyzeData import analyze_data

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'csv'}

# app.config["UPLOAD_FOLDER"] = "/var/www/data2int.com/html/templates/uploadedFiles"
app.config["UPLOAD_FOLDER"] = "H:/School/New Semester/Data2Int/Test-File/Uploaded-Files"
# app.config["UPLOAD_FOLDER"] = "C:/Users/dante/Desktop/PROJECT CLASS/data2int/Data2Int/html/templates/dante"
# app.config["UPLOAD_FOLDER"] = "/mnt/c/Users/Hamza/Desktop/Data2Int-GitHub/Data2Int/html/templates/uploaded_files"
app.config["MAX_FILE_SIZE"] = 10485760

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'donorschoose'
COLLECTION_NAME = 'projects'
FIELDS = {'school_state': True, 'resource_type': True, 'poverty_level': True, 'date_posted': True, 'total_donations': True, '_id': False}
file_name = ""
column_list = {}


# def max_filesize(filesize):
#     if int(filesize) <= app.config["MAX_FILE_SIZE"]:
#         return true
#     else:
#         return false

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/Upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':

        # if max_filesize(request.cookies.get("filesize")):
        #     return render_template('ErrorFileUpload.html')

        uploaded_file = request.files['file']

        duplicatesInput = request.form['radioButton']

        print(duplicatesInput)

        # File name can not be null
        if uploaded_file.filename == "":
            return render_template('ErrorFileUpload.html')

        # Kevin's edit
        # Get the extension
        extension = os.path.splitext(uploaded_file.filename)[1]
        filename = os.path.basename(uploaded_file.filename)
        collectionName = os.path.splitext(uploaded_file.filename)[0]
        global file_name
        file_name = collectionName

        # Sanitary check the file extension
        # If the file extension .csv or .xlsx or .xml
        # Case 1
        if extension == ".csv" or extension == ".xlsx" or extension == ".xml":
            clean_database(collectionName, MONGODB_HOST, MONGODB_PORT, DBS_NAME)
            upload_success = upload(extension, filename, uploaded_file, app.config["UPLOAD_FOLDER"], duplicatesInput, MONGODB_HOST, MONGODB_PORT, DBS_NAME)
            analyzed_columns = analyze_data(filename, app.config["UPLOAD_FOLDER"], MONGODB_HOST, MONGODB_PORT, DBS_NAME)
            global column_list
            column_list = analyzed_columns
            for analyzed in analyzed_columns.items():
                print(analyzed)
        
            if not upload_success:
                return render_template("ErrorFileUpload.html")

        # If the file extension .json
        elif extension == ".json":
            clean_database(collectionName, MONGODB_HOST, MONGODB_PORT, DBS_NAME)
            print("Case 2: This file extension is " + extension)
            uploaded_file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            with open(app.config["UPLOAD_FOLDER"] + "/" + filename) as json_file:
                json_data = json.load(json_file)

            # scan the file for a virus
            has_virus = virus_scan(uploaded_file, app.config["UPLOAD_FOLDER"])

            # check the scan result
            if has_virus:
                # Check if the file exists at the specified directory first before deleting
                if os.path.exists(app.config["UPLOAD_FOLDER"] + "/" + filename):
                    os.remove(app.config["UPLOAD_FOLDER"] + "/" + filename)
                    return render_template("ErrorFileUpload.html")

            json_upload(json_data, filename, duplicatesInput, MONGODB_HOST, MONGODB_PORT, DBS_NAME)
            # Json file upload
        # Everything else
        # Render error file upload page
        else:
            print("Case 3: This file extension is '" + extension + "'. File upload error")
            return render_template("ErrorFileUpload.html")

        raw_data = fetchData(collectionName, MONGODB_HOST, MONGODB_PORT, DBS_NAME)
        preview_data = getPreviewData(raw_data)
        #return render_template('SuccessfulUpload.html', tables=[preview_data.to_html(classes='data', header='true')])
        return redirect(url_for('success_file_upload', fileName = file_name))


@app.route('/ErrorFileUpload')
def error_file_upload():
    return render_template('ErrorFileUpload.html')


@app.route('/Upload')
def upload_file_page():
    return render_template('UploadPage.html')


@app.route('/SuccessfulUpload/<fileName>')
def success_file_upload(fileName):
    print(fileName)
    return render_template('SuccessfulUpload.html', collectionname=fileName)


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
def accessing_data():
    # connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    # json_collection = connection[DBS_NAME]["test"]
    # testfile = open("/var/www/data2int.com/html/templates/uploadedFiles/Test.json")
    # json_data = json.load(testfile)
    # for i in json_data:
    #    json_collection.insert_one(i)
    # testfile.close()
    # connection.close()
    return render_template('AccessingData.html')


@app.route('/MovingData')
def moving_data():
    return render_template('MovingData.html')


@app.route('/FindingData')
def finding_data():
    return render_template('FindingData.html')


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
def meeting_minutes():
    return render_template('MeetingMinutes.html')


@app.route('/DocumentLibrary')
def document_library():
    return render_template('DocumentLibrary.html')


@app.route('/Programmer1')
def programmer1():
    return render_template('Programmer1.html')


@app.route('/Programmer2')
def programmer2():
    return render_template('Programmer2.html')


@app.route('/Programmer3')
def programmer3():
    return render_template('Programmer3.html')


@app.route('/Programmer4')
def programmer4():
    return render_template('Programmer4.html')


@app.route('/Programmer5')
def programmer5():
    return render_template('Programmer5.html')


@app.route('/DevEnv')
def dev_env():
    return render_template('DevEnv.html')


@app.route('/MongoDB')
def mongo_db():
    return render_template('MongoDB.html')


@app.route('/Flask')
def flask():
    return render_template('Flask.html')


@app.route('/D3')
def d3():
    return render_template('D3.html')


@app.route('/Dc')
def dc():
    return render_template('Dc.html')


@app.route('/Folium')
def folium():
    return render_template('Folium.html')


@app.route('/Prism')
def prism():
    return render_template('Prism.html')


@app.route('/BigData')
def big_data():
    return render_template('BigData.html')


@app.route('/Paraquet')
def paraquet():
    return render_template('Paraquet.html')


@app.route('/Clusters')
def clusters():
    return render_template('Clusters.html')


@app.route('/UsefulResources')
def useful_resources():
    return render_template('UsefulResources.html')


@app.route('/numpy')
def num_py():
    return render_template('numpy.html')


@app.route('/pandas')
def pandas():
    return render_template('pandas.html')


@app.route('/scipy')
def scipy():
    return render_template('scipy.html')


@app.route('/keras')
def keras():
    return render_template('keras.html')


@app.route('/scikitlearn')
def scikitlearn():
    return render_template('scikitlearn.html')


@app.route('/pytorch')
def pytorch():
    return render_template('pytorch.html')


@app.route('/tensorflow')
def tensorflow():
    return render_template('tensorflow.html')


@app.route('/MachineLearning')
def machine_learning():
    return render_template('MachineLearning.html')


@app.route('/PredictiveModeling')
def predictive_modeling():
    return render_template('PredictiveModeling.html')


@app.route('/DataMining')
def data_mining():
    return render_template('DataMining.html')


@app.route('/mathplotlib')
def mathplotlib():
    return render_template('matplotlib.html')


@app.route('/seaborn')
def seaborn():
    return render_template('seaborn.html')


@app.route('/bokeh')
def bokeh():
    return render_template('bokeh.html')


@app.route('/plotly')
def plotly():
    return render_template('plotly.html')


@app.route('/pydot')
def pydot():
    return render_template('pydot.html')


@app.route('/charts')
def charts():
    return render_template('charts.html')


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


@app.route("/donorschoose/mapdata")
def donorschoose_mapdata():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME]["MapData"]

    # MAP_FIELDS = {'GEO_CODE (POR)': True, 'GEO_NAME': True, 'DIM: Profile of Census Divisions (2247)': True,
    # 'Dim: Sex (3): Member ID: [1]: Total - Sex': True}
    # projects = collection.find(projection=FIELDS, limit=100000)

    mapData = collection.find({ "DIM: Profile of Census Divisions (2247)": "Population, 2016" })
    
    json_mapdata = []
    for data in mapData:
        json_mapdata.append(data)
    json_mapdata = json.dumps(json_mapdata, default=json_util.default)
    connection.close()
    # print(json_mapdata)
    return json_mapdata

@app.route("/donorschoose/mapdataupdate")
def donorschoose_mapadata_geoname():

    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME]["MapData"]
    data_filter = {"Dim: Sex (3): Member ID: [1]: Total - Sex" : {"$ne": "0"}}

    mapData = collection.find(data_filter)
    json_mapdata = []
    for data in mapData:
        json_mapdata.append(data)
    json_mapdata_final = json.dumps(json_mapdata, default=json_util.default)
    connection.close()

    return json_mapdata_final

####################################################################################################################
@app.route("/donorschoose/scatterplot")
def donorschoose_scatterplot():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][file_name]

    data = collection.find()
    
    json_data = []
    for data in data:
        json_data.append(data)
    json_data = json.dumps(json_data, default=json_util.default)
    connection.close()
    # print(json_mapdata)
    return json_data

####################################################################################################################
@app.route("/donorschoose/scatterplotmeasures")
def donorschoose_scatterplot_measures():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][file_name]
    var1 = ""
    var2 = ""
    xVar = ""
    yVar = ""
    ################ var1 & var2 values #################
    for i in column_list.items():
        if(i[1]== "measure"):
            if (var1 == ""):
                var1 = i[0]
            else:
                var2 = i[0]

    if(var1 != ""):
        var1field = {var1 : True, "_id" : False}
        var1Val = collection.find(projection=var1field).sort(var1).collation({ 'locale': "en_US", 'numericOrdering': True }).limit(1)
        for i in var1Val:
            for j in i.values():
                var1Min = j
        var1Val = collection.find(projection=var1field).sort(var1, -1).collation({ 'locale': "en_US", 'numericOrdering': True }).limit(1)
        for i in var1Val:
            for j in i.values():
                var1Max = j
    if(var2 != ""):
        var2field = {var2 : True, "_id" : False}
        var2Val = collection.find(projection=var2field).sort(var2).collation({ 'locale': "en_US", 'numericOrdering': True }).limit(1)
        for i in var2Val:
            for j in i.values():
                var2Min = j
        var2Val = collection.find(projection=var2field).sort(var2, -1).collation({ 'locale': "en_US", 'numericOrdering': True }).limit(1)
        for i in var2Val:
            for j in i.values():
                var2Max = j
    ###########################################

    if(var1Max > var2Max):
        yVar = var1
        yMax = var1Max
        yMin = var1Min
        xVar = var2
        xMax = var2Max
        xMin = var2Min
    else:
        yVar = var2
        yMax = var2Max
        yMin = var2Min
        xVar = var1
        xMax = var1Max
        xMin = var1Min

    ################ z values #################
    zVar = ""
    for i in column_list.items():
        if(i[1]== "largestMeasure"):
            zVar = i[0]

    zfield = {zVar : True, "_id" : False}
    zVal = collection.find(projection=zfield).sort(zVar).collation({ 'locale': "en_US", 'numericOrdering': True }).limit(1)
    for i in zVal:
        for j in i.values():
            zMin = j
    zVal = collection.find(projection=zfield).sort(zVar, -1).collation({ 'locale': "en_US", 'numericOrdering': True }).limit(1)
    for i in zVal:
        for j in i.values():
            zMax = j
    ###########################################
    print("X: " + xVar + " Max: " + xMax + " Min: " + xMin)
    print("Y: " + yVar + " Max: " + yMax + " Min: " + yMin)
    print("Z: " + zVar + " Max: " + zMax + " Min: " + zMin)
    data = {"x": xVar, "xMin":xMin, "xMax":xMax, "y": yVar, "yMin":yMin, "yMax":yMax,"z": zVar, "zMin":zMin, "zMax":zMax}
    
    json_data = json.dumps(data, default=json_util.default)
    connection.close()
    return json_data
####################################################################################################################
@app.route("/donorschoose/scatterplotdimensions")
def donorschoose_scatterplot_dimensions():

    dimensions = []
    for i in column_list.items():
        if(i[1] == "dimension"):
            dimensions.append(i[0])
    json_data = json.dumps(dimensions, default=json_util.default)
    print(json_data)
    return json_data

####################################################################################################################

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
