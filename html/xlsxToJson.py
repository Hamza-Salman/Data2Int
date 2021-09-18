import pandas

# sheet_name='Book1'
excel_data_df = pandas.read_excel('/var/www/data2int.com/html/templates/uploadedFiles/sampleXLSX.xlsx')
json_str = excel_data_df.to_json('/var/www/data2int.com/html/templates/uploadedFiles/sampleXLSXToJson.json')


