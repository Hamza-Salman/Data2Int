import requests
import os
import json


def virus_scan(uploaded_file, filepath) -> bool:
    # create the end point to send the request to
    endpoint = "https://api.virusscannerapi.com/virusscan"

    # filepath: str = "C:/Users/Mark/PycharmProjects/pythonProject/venv/templates/uploadedFiles/"
    # filepath: string = "/var/www/data2int.com/html/templates/uploadedFiles"

    # create the request header with the ID and secret key from your account
    headers = {
        'X-ApplicationID': '0c62195a-e25e-40c6-86df-0b56bd707dc6',
        'X-SecretKey': '4b458de7-4844-41ea-9372-513716a6919a'
    }

    # grab the file name
    filename = uploaded_file.filename

    # Grab the size of the file at the requested location's size in bytes
    file_byte_size = os.path.getsize(filepath + "/" + filename)

    # Convert to kilobytes by dividing by 1024
    filesize: int = file_byte_size / 1024

    # open the file
    file = open(filepath + "/" + filename, "rb")

    # define as a synchronous process
    data = {
        'async': 'false',
    }

    # Check if the estimated filesize is greater than or equal to 50000 KB
    if filesize >= 50000:
        # Read the file up to half the filesize to insert into the request content
        files = {
            'inputFile': ('\'' + filename + '\'', file.read(int(filesize/2)))
        }
    else:
        # add the file to the dictionary, reading the whole file to insert as the request content
        files = {
            'inputFile': ('\'' + filename + '\'', file.read())
        }

    file.close()

    # await the response using a POST request
    r = requests.post(url=endpoint, data=data, headers=headers, files=files)

    # Ensure the response's status code is OKAY
    if r.status_code == 200:
        # convert the JSON response text into a dictionary
        response = json.loads(r.text)

        # Check the string for the status. Files without any issues will return "File is clean"
        if response["status"] != "File is clean":
            # virus/malware found in file
            return True

    return False
