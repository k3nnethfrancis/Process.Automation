#! python3

# This is a standard ETL process
# This script is designed to extract a file from an (S)FTP server (filezilla)
# Save the file locally
# Transform the Data
# And load it back to the (S)FTP
# The LMS will pick up the file daily from there

# Import modules
import sys
import os
import pysftp
import pandas as pd

# DEFINING FUNCTIONS
# DOWNLOAD DATA FROM SFTP SERVER AND LOAD IT TO A DATAFRAME

def sftp_download(path_name, file_name, local_path, local_file_name):
    '''
    Takes path and file names as arguements, connects to sftp, downloads a file, and writes it to a dataframe
        Parameters:
                path_name: path in SFTP server where file is located
                file_name: file name in SFTP server
                local_path: path where the file will be downloaded
                local_file_name: what the file will be named when downloaded
        Returns:
            dataframe of file
        Notes:
            Must be an csv file.
    '''
    # Define Credential Variables
    HOST = 'ftp.hostname.com'
    USER = 'user'
    PASS = os.environ['SFTP_PASS']
    
    # Define File Location (from user input)
    PATH = path_name
    FILE = file_name

    # Establish Connection
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = cnopts.hostkeys.load(r'C:\Users\...\SFTP_Host_keys.txt')  # This should be the path of the .txt file that contains your host keys
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

# UPLOAD A FILE TO AN SFTP

def sftp_upload(remote_path, remote_file_name, local_path, local_file_name):
    '''
    Takes path and file names as arguements, connects to sftp, and uploads a file
        Parameters:
                remote_path: path in SFTP server where file will be uploaded
                remote_file_name: name for file to be uploaded to SFTP server
                local_path: path where the file to be uploaded is located
                local_file_name: name of the file being uploaded
        Returns:
                None
    '''
    # Define Credential Variables
    HOST = 'ftp.hostname.com'
    USER = 'user'
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

export_df = sftp_download(DLremote_path, DLremote_file_name, local_path, local_file_name)

# TRANSFORM THE DATAFRAME

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
IDdf = LMS_df[['custom_field: Employee Number', 'Email']]                               # create a new df of IDs and emails only
IDdf = IDdf.rename(columns={'custom_field: Employee Number': 'MgrNumber',               # rename columns for join
                                        'Email': 'custom_field: Manager E-mail'})

mdf = LMS_df[['custom_field: Manager Employee Number']].drop_duplicates()               # create a new df of manager IDs and drop duplicates
mdf = mdf.rename(columns={'custom_field: Manager Employee Number': 'MgrNumber'})        # rename columns for join

inner_join_df= pd.merge(mdf, IDdf, on=['MgrNumber'], how='inner')                       # join emails to manager IDs to get manager emails
inner_join_df.drop_duplicates()                                                         

LMS_df1 = LMS_df.rename(columns={'custom_field: Manager Employee Number': 'MgrNumber'}) # create a new df from the original df and match column names for join
LMS_df1 = LMS_df1.drop(columns='custom_field: Manager E-mail')                          # drop the manager email column (will be replaced when joined)

LMS_df = pd.merge(LMS_df1, inner_join_df, how='inner')

LMS_df = LMS_df.rename(columns={'MgrNumber':'custom_field: Manager Employee Number'})   # rename new columns to meet requirements

neworder = ['Login', 'Firstname', 'Lastname', 'Email', 'Password', 'User-type',
       'Bio', 'Active', 'Deactivation-date', 'Exclude-from-emails',
       'custom_field: Common Name', 'custom_field: Employee Number',
       'custom_field: Job Level', 'custom_field: Department',
       'custom_field: System', 'custom_field: Manager Name',
       'custom_field: Manager Employee Number', 'custom_field: Manager E-mail',
       'custom_field: Pay Type', 'custom_field: State']

LMS_df=LMS_df.reindex(columns=neworder)                                                 # reorder columns to meet requirements

#WRITE THE TRANSFORMED DATAFRAME TO A NEW FILE
path = local_path + local_file_name
LMS_df.to_excel(path, index=False)

# RE-UPLOAD THE FILE TO SFTP
sftp_upload(ULremote_path, ULremote_file_name, local_path, local_file_name)
