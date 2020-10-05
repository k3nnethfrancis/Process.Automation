#! python3

# #import modules
import sys
import os
import pysftp
import pandas as pd

# DOWNLOAD DATA FROM FILEZILLA SERVER AND LOAD IT TO A DATAFRAME

def fzilla_download(path_name, file_name, local_path, local_file_name):
    '''
    Takes path and file names as arguements, connects to filezilla, downloads a file, and writes it to a dataframe
        Parameters:
                path_name: path in SFTP server where file is located
                file_name: file name in SFTP server
                local_path: path where the file will be downloaded
                local_file_name: what file will be named when downloaded
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

path_name= r'/SFTP/Server/Path'
file_name= r'/file_name_on_server.csv'
local_path= r"C:\Users\....\path"
local_file_name= r"\file_name.csv"

df = fzilla_download(path_name, file_name, local_path, local_file_name)
