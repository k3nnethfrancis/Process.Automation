def DF_api(report_name):
    '''
    Takes a report integration name report_name, sends a get request, parses json, and returns a dataframe.
        Parameters:
                report_name: report integration name 
        Returns:
            dataframe of said report.
        Notes:
            Dayforce report must be a V2 report.
            Row Limit: 5000
    '''

    # import necessary modules
    import requests
    import pandas as pd
    import json
    import os

    # get credentials from environment variables
    USER = os.environ['DF_USER']
    PASS = os.environ['DF_PASS']

    report = report_name

    url = r"https://usr58-services.dayforcehcm.com/Api/Motivate/V1/Reports/" + report

    # perform get request to obtain json data

    r = requests.get(url , auth=(USER, PASS))

    # convert json to a datafram

    r_json = r.json()
    df = pd.DataFrame.from_dict(r_json['Data']['Rows'])
    return df

my_report = DF_api("report_integration_name")

# Optional: Write the DataFrame to a .csv file
#my_report.to_csv(r"C:\Users\PATH...\Desktop\FileName.csv", index=False)
       
