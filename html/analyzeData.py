import csv

def analyze_data(uploaded_file, path_to_file):
    print(uploaded_file)
    print(path_to_file)
    csvFile = open(path_to_file + "/" + uploaded_file, 'r')
    reader = csv.DictReader(csvFile)
    with open(path_to_file + "/" + uploaded_file) as csv_file:
        csvReader = csv.reader(csv_file, delimiter=',')
        list_of_columns = []
        for row in csvReader:
            list_of_columns.append(row)
            break

    for each in reader:
        row = {}
        for field in list_of_columns[0]:
            print(field)
