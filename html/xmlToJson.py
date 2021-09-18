import json
import xmltodict

with open("/var/www/data2int.com/html/templates/uploadedFiles/sampleXML.xml") as xml_file:  # Open targeted file
    data_dict = xmltodict.parse(xml_file.read())  # Load XML data into dictionary datatype
    # In python, you can have something like this: map = { "1" : "Kevin", "2" : "Hamza"}
    xml_file.close();  # Close XML file to reduce the risk of being unwarranted modified or read.

    json_data = json.dumps(data_dict)  # json.dumps() take a json object and returns a string

    with open("/var/www/data2int.com/html/templates/uploadedFiles/sampleXMLtoJSON.json", "w") as json_file:
        # Create new file and write our data into that file
        json_file.write(json_data)
        json_file.close()
