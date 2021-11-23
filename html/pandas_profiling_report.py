import numpy as np
import pandas as pd
from uploadData import upload
from pandas_profiling import ProfileReport
import pandas as pd
import webbrowser
from pymongo import MongoClient
import os

def generate_report(num_measures, upload_path, df, fileName) -> bool:
    if(df.empty): 
        print("Dataframe is empty")
        return False


    _title = fileName + " Profiling Report"
    if num_measures <= 5:
        profileReport = ProfileReport(df, title=_title, explorative=True)
    else:
        profileReport = ProfileReport(df, title=_title, minimal=True)
        
    collectionName = os.path.splitext(fileName)[0]
    reportHTML = upload_path + "/" + collectionName + "_report.html"
    report_file = profileReport.to_file(reportHTML)
    # webbrowser.open_new_tab(reportHTML)
    return True
