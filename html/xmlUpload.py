import xml.etree.ElementTree as ET
from calcDeleteTime import seconds_until_end_of_day

import random

from pymongo import MongoClient


def xml_upload(uploaded_file, path_to_file, duplicatesInput, DB_HOST, DB_PORT, DB_Name):
    # Define constants
    COLLECTION_NAME = uploaded_file.split('.')[0]
    # print(COLLECTION_NAME)

    connection = MongoClient(DB_HOST, DB_PORT)

    collection = connection[DB_Name][COLLECTION_NAME]

    index_num = random.randint(0, 10000)
    index_name = "expire_date_time_" + str(index_num)

    with open(path_to_file + "/" + uploaded_file) as xml_file:  # Open targeted file
        tree = ET.parse(path_to_file + "/" + uploaded_file)
        # print(tree)

        root = tree.getroot()
        # print(rootName)

        elementName = root[0].tag
        # print(elementName)

        stud = tree.findall(elementName)
        for i in stud:
            print(i)

        childTags = []
        for child in stud[1]:
            childTags.append(child.tag)

        # for item in childTags:
        #    print(item)

        if (duplicatesInput == "NoDupes"):
            no_dupes = []
            for rows in stud:
                data_dict = {}
                for cols in childTags:
                    data_dict[cols] = rows.find(cols).text

                if data_dict not in no_dupes:
                    no_dupes.append(data_dict)

            collection.create_index(index_name, expireAfterSeconds=seconds_until_end_of_day())
            collection.insert_many(no_dupes)
        else:
            for rows in stud:
                data_dict = {}
                for cols in childTags:
                    data_dict[cols] = rows.find(cols).text

                collection.create_index(index_name, expireAfterSeconds=seconds_until_end_of_day())
                collection.insert(data_dict)

        xml_file.close()  # Close XML file to reduce the risk of being unwarranted modified or read.
        connection.close()








