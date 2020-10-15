#! python

# Refresh the data connection, Load the file, manipulate the dataframe, send an email with the info

# Import Packages
import Refresh_Excel
import Email_DF
import pandas as pd

#PART 1: REFRESH THE DATA CONNECTION IN THE EXCEL WORKBOOK

file_path = r'C:\Users\username\Desktop\PATH\FileName.xlxs'  # Input your workbook's path here

refresh_excel(file_path=file_path)                                                        

#PART 2: LOAD IN THE FILE AND TRANSFORM DATA

df = pd.read_excel(file_path)                           # Read in the file

data = df[['Column_A', 'Column_B']]                     # Create a new dataframe with only the columns we want to report on
                                                        # Replace with your columns
data = df.rename(columns={'Column_A': 'New_Col_Name', 'Column_B':'New_Col_Name_B'}) # Rename Your Columns to make them more readable (Optional)


#PART 3: SEND AN EMAIL WITH THE DATA WE SELECTED

host = 'smtp.gmail.com'                                  # Smtp connection domain for gmail
email = 'email@domain.com'                               # Email of the associated account which will be used for login credentials
pw = 'pw'                                                # Password for login credentials
recipients = ['email@domain.com']                        # Who the email will be sent to. Can be one or multiple people in the list

email_df(data=data, host=host, email=email, pw=pw, recipients=recipients, subject='your_subject' From=email)
