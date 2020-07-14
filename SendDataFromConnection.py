# Refresh the data connection, Load the file, manipulate the dataframe, send an email with the info

# Import Packages

import win32com.client                                  # For working with excel files and refreshing the connection
import pandas as pd                                     # For Data manipulation
import smtplib                                          # For Sending emails
from email.mime.text import MIMEText                    # MIME helps us format emails
from email.mime.application import MIMEApplication      # MIME also allows us to email data in a tabular (or DF) format 
from email.mime.multipart import MIMEMultipart          
from datetime import date                               # For adding todays date into the subject line


#PART 1: REFRESH THE DATA CONNECTION IN THE EXCEL WORKBOOK

path = r'C:\Users\username\Desktop\PATH\FileName.xlxs'  # Input your workbook's path here

xlapp = win32com.client.DispatchEx("Excel.Application") # Start an instance of Excel

wb = xlapp.workbooks.open(path)                         # Open the workbook

wb.RefreshAll()                                         # Refresh all data connections in said workbook

xlapp.CalculateUntilAsyncQueriesDone()                  # Holds the program until the refresh has completed

xlapp.DisplayAlerts = False                             # Stops the dialog box from popping up

wb.Save()                                               # Saves the file

xlapp.Quit()                                            # Quits the connection


#PART 2: LOAD IN THE FILE AND TRANSFORM DATA

df = pd.read_excel(path)                                # Read in the file

data = df[['Column_A', 'Column_B']]                     # Create a new dataframe with only the columns we want to report on
                                                        # Replace with your columns
data = df.rename(columns={'Column_A': 'New_Col_Name', 'Column_B':'New_Col_Name_B'}) # Rename Your Columns to make them more readable (Optional)


#PART 3: SEND AN EMAIL WITH THE DATA WE SELECTED

host = 'smtp.gmail.com'                                  # Smtp connection domain for gmail
email = 'email@domain.com'                               # Email of the associated account which will be used for login credentials
pw = 'pw'                                                # Password for login credentials
recipients = ['email@domain.com']                        # Who the email will be sent to. Can be one or multiple people in the list
#emaillist = [elem.strip().split(',') for elem in recipients]   # If you want to send to multiple recipients, will parse from the above list

msg = MIMEMultipart()                                       # Variable to initiate the MIME function for inputting different pieces of the email
today = date.today()                                        # Todays date unformatted (for use in the subject)
d2 = today.strftime("%B %d, %Y")                            # Todays date formatted as textual month, then day and year (e.g. 'July 13, 2020')
msg['Subject'] = 'Your Data as of ' + str(d2)  # Subject line
msg['From'] = 'email@domain.com'                            # Who the email is being sent from (probably same as the email variable)

# This bit formats the DF into an html format

html = """\
<html>
  <head></head>
  <body>
    {0}
  </body>
</html>
""".format(data.to_html())                            # This is what allows the DF to appear as a table in the email
                                                      # Note the data.to_html method

part1 = MIMEText(html, 'html')                        # Further html formatting
msg.attach(part1)

# The bit that actually sends the email

con = smtplib.SMTP(host, 587)                          # Connection variable
con.ehlo()                                             # Starts the connection
con.starttls()                                         # Starts the encryption
con.login(email, pw)                                   # Logs you in      
con.sendmail(msg['From'], recipients , msg.as_string())# Sends your email, change recipients to emaillist if sending to multiple recipients
con.quit()                                             # Quits the connection
