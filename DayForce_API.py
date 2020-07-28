# Importing Librarys

import requests
import pandas as pd
import json
import os

# Get credentials from environment variabels
USER = os.environ['DF_USER']
PASS = os.environ['DF_PASS']

# Select report and concatenate to url string
report = "API_TEST"
url = r"https://usr58-services.dayforcehcm.com/Api/companyname/V1/Reports/" + report

# Create a response object that contains our report data
r = requests.get(url , auth=(USER, PASS)) 

# Decode json from response object
r_json = r.json()

# Parse json into a data frame
# for r_json['Data']['Rows'] we are selecting the dict Rows within the outer dict 'Data'
df = pd.DataFrame.from_dict(r_json['Data']['Rows'])

# Print the DataFrame to confirm
print(df)

# Optional: Write the DataFrame to a .csv file
#df.to_csv(r"C:\Users\PATH...\Desktop\FileName.csv", index=False)
       
