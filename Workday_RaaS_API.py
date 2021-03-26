#! python3 

# import modules
import os
import json
import requests
import pandas as pd

def WD_api(url):
    '''
    Utilizes RaaS feature of workday to takes a workday webservices url, send a get request, parse json, and return a dataframe.
        Parameters:
                url: web_services report url
        Returns:
            dataframe of said report.
    '''
    # get credentials from environment variables
    USER = "workday username"
    PASS = "workday password"

    # perform get request to obtain json data

    r = requests.get(url , auth=(USER, PASS))

    # convert json to a datafram

    r_json = r.json()
    df = pd.DataFrame.from_dict(r_json['Report_Entry'])
    return df

url = "your reports webservices url"
report = WD_api(url)


print(report)

# Optional: Write the DataFrame to a .csv file
#my_report.to_csv(r"C:\Users\PATH...\Desktop\FileName.csv", index=False)

