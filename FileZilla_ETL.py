#! python3

# This is a standard ETL process
# This script is designed to extract a file from an (S)FTP server (filezilla)
# Save the file locally
# Transform the Data
# And load it back to the (S)FTP
# The LMS will pick up the file daily from there

# DOWNLOAD DATA FROM FILEZILLA SERVER AND LOAD IT TO A DATAFRAME

def fzilla_download(path_name, file_name, local_path, local_file_name):
    #import modules
    import pysftp
    import sys
    import pandas as pd
    import os

    # Define Credential Variables
    HOST = ''
    USER = ''
    PASS = os.environ['SFTP_PASS']
    
    # Define File Location (from user input)
    PATH = path_name
    FILE = file_name

    # Establish Connection
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = cnopts.hostkeys.load('SFTP_Host_keysTEST.txt') # This should be the path of the text file that contains your host keys
                                                                     # If you don't have them, replace it with cnopts.hostkeys = None
    srv = pysftp.Connection(HOST, USER, password=PASS, cnopts=cnopts)

    # Define Local Path (for download destination)
    LFN = local_file_name
    LP = local_path
    full_local_path = LP + LFN

    # Download File To Local Path
    srv.get(PATH + FILE, full_local_path)

    # Close Connection
    srv.close()

    # Create a Dataframe From Local File
    df = pd.read_csv(full_local_path)
    
    return df

# UPLOAD FILE TO SFTP

def fzilla_upload(remote_path, remote_file_name, local_path, local_file_name):
    #import modules
    import pysftp
    import sys
    import pandas as pd
    import os

    # Define Credential Variables
    HOST = ''
    USER = ''
    PASS = os.environ['SFTP_PASS']
    
    # Define File Location (from user input)
    RP = remote_path
    RF = remote_file_name
    LP = local_path
    LF = local_file_name
    full_remote_path = RP + RF
    full_local_path = LP + LF

    # Establish Connection
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = cnopts.hostkeys.load('SFTP_Host_keysTEST.txt') # This should be the path of the text file that contains your host keys
                                                                     # If you don't have them, replace it with cnopts.hostkeys = None
    srv = pysftp.Connection(HOST, USER, password=PASS, cnopts=cnopts)

    # Load File to SFTP
    srv.put(full_local_path, full_remote_path)

    # Close Connection
    srv.close()

    return


# DEFINE PATH VARIABLES

DLremote_path= ''                 # Path name from (S)FTP where you are downloading the file from
DLremote_file_name= ''            # Name of the file you are downloading from (S)FTP
ULremote_path= ''                 # Path name from (S)FTP where you are uploading the file to
ULremote_file_name= ''            # Name of the file you are uploading to (S)FTP
local_path= ''                    # Local desitination of the extracted file
local_file_name= ''               # Local file name

# DOWNLOAD THE FILE AND LOAD IT OT A DATAFRAME

export_df = fzilla_download(DLremote_path, DLremote_file_name, local_path, local_file_name)

# TRANSFORM THE DATAFRAME

#Import modules
import pandas as pd

#Initialize the import DataFrame
import_df = pd.DataFrame(columns=['Login', 'Firstname', 'Lastname', 'Email', 'Password', 'User-type',
       'Bio', 'Active', 'Deactivation-date', 'Exclude-from-emails',
       'custom_field: Common Name', 'custom_field: Employee Number',
       'custom_field: Job Level', 'custom_field: Department',
       'custom_field: System', 'custom_field: Manager Name',
       'custom_field: Manager Employee Number', 'custom_field: Manager E-mail',
       'custom_field: Pay Type', 'custom_field: State'])

#Begin Tranformation
#Most are 1 to 1 transformations
#The lines commented out can either be NaN or need a custom transformation
#In this example I am working with HRIS data and transforming to fit LMS requirements
LMS_df = import_df

LMS_df['Login'] = export_df['username']
LMS_df['Firstname'] = export_df['firstname']
LMS_df['Lastname'] = export_df['lastname']
LMS_df['Email'] = export_df['email']
# LMS_df['Password'] = NaN
LMS_df['User-type'] = LMS_df['User-type'].fillna('Learner')
LMS_df['Bio'] = export_df['jobTitle']
LMS_df['Active'] = LMS_df['Active'].fillna('YES')
# LMS_df['Deactivation-date'] = NaN
LMS_df['Exclude-from-emails'] = LMS_df['Exclude-from-emails'].fillna(False)
LMS_df['custom_field: Common Name'] = export_df['common_name']
LMS_df['custom_field: Employee Number'] = export_df['employee_id']
# LMS_df['custom_field: Job Level'] = custom xform
LMS_df['custom_field: Department'] = export_df['department']
LMS_df['custom_field: System'] = export_df['location'] # will also need custom xform to change to systems
LMS_df['custom_field: Manager Name'] = export_df['manager name']
LMS_df['custom_field: Manager Employee Number'] = export_df['manager id']
# LMS_df['custom_field: Manager E-mail'] = custom xform
LMS_df['custom_field: Pay Type'] = export_df['paytype']
LMS_df['custom_field: State'] = export_df['location_state']

#Transform Job Levels
level = []                                                             # initialize an empty list
for i in LMS_df['custom_field: Employee Number'].to_list():            # iterate through employee number as a list
    if i in LMS_df['custom_field: Manager Employee Number'].to_list(): # check if employee number is in mgr num col 
        level.append('Manager')                                        # if so, add the word manager to the list: level
    else:                                                              # otherwise, add the word employee
        level.append('Employee')

LMS_df['custom_field: Job Level'] = level                              # input level list into job level column

#Transform Systems
#Renaming locations to broader system names
#Note that this can be done in less lines of code, but I did it line by line for readability
LMS_df['custom_field: System'] = LMS_df['custom_field: System'].replace(['Loc1'],'System1')
LMS_df['custom_field: System'] = LMS_df['custom_field: System'].replace(['Loc2'],'System2')
LMS_df['custom_field: System'] = LMS_df['custom_field: System'].replace(['Loc3'],'System3')
LMS_df['custom_field: System'] = LMS_df['custom_field: System'].replace(['Loc4'],'System4')
LMS_df['custom_field: System'] = LMS_df['custom_field: System'].replace(['Loc5'],'System5')

#Transform Manager Email
#This looks at an employees manager id, checks for where it is in the employee ID column
#And then populates the email of that manager in the manager email column based off the index
MgrIndex = []                                                                             # initialize an empty list
for i in LMS_df['custom_field: Manager Employee Number'].to_list():                       # iterate through maanger number as a list
    if i in LMS_df['custom_field: Employee Number'].to_list():                            # check if mgr num exists in the list of employee nums
        MgrIndex.append(LMS_df[LMS_df['custom_field: Employee Number']==i].index.values)  # return the index of the manager num in employee nums
                                                                                          # and append to the list MgrIndex                                                                                        
                                                                                          
MgrEmail = []                                                                             # initialize an empty list
for i in MgrIndex:                                                                        # iterate through the MgrIndex list
    MgrEmail.append(list(LMS_df['Email'][i]))                                             # append the email at the index in MgrIndex
LMS_df['custom_field: Manager E-mail'] = pd.DataFrame(MgrEmail)                           # input MgrEmail list into Manager Email Column
                                                                                          # note that here MgrEmail must be converted to a DF

#WRITE THE TRANSFORMED DATAFRAME TO A NEW FILE
path = local_path + local_file_name
LMS_df.to_excel(path, index=False)

# RE-UPLOAD THE FILE TO SFTP
fzilla_upload(ULremote_path, ULremote_file_name, local_path, local_file_name)
