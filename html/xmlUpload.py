import xml.etree.ElementTree as ET

from pymongo import MongoClient


def xml_upload(uploaded_file, path_to_file, DB_HOST, DB_PORT, DB_Name):
    # Define constants
    COLLECTION_NAME = uploaded_file.split('.')[0]
    # print(COLLECTION_NAME)

    connection = MongoClient(DB_HOST, DB_PORT)

    collection = connection[DB_Name][COLLECTION_NAME]

    with open(path_to_file + "/" + uploaded_file) as xml_file:  # Open targeted file
        tree = ET.parse(path_to_file + "/" + uploaded_file)
        # print(tree)

        root = tree.getroot()
        rootName = root.tag
        # print(rootName)

        elementName = root[0].tag
        # print(elementName)

        stud = tree.findall(elementName)

        childTags = []
        for child in stud[1]:
            childTags.append(child.tag)

        # for item in childTags:
        #    print(item)

        for rows in stud:
            data_dict = {}
            for cols in childTags:
                data_dict[cols] = rows.find(cols).text
            x = collection.insert(data_dict)

        xml_file.close()  # Close XML file to reduce the risk of being unwarranted modified or read.
        connection.close()
