import numpy as np
import pandas as pd
from uploadData import upload
from pandas_profiling import ProfileReport
import pandas as pd
import webbrowser
from pymongo import MongoClient

def generate_report(df, fileName) -> bool:
    if(df.empty): 
        print("Dataframe is empty")
        return False

    _title = fileName + " Profiling Report"
    profileReport = ProfileReport(df, title=_title, explorative=True)
    reportHTML = "/html/templates/uploaded_report/" + fileName + "_report.html"
    report_file = profileReport.to_file(reportHTML)
    webbrowser.open_new_tab(reportHTML)
    return True
