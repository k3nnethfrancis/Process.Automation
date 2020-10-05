#! python3

#  #import modules
import sys
import os
import pandas as pd
import pysftp

## UPLOAD A FILE TO AN SFTP

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

remote_path= r'/SFTP/Server/Path'
remote_file_name= r'/file_name_on_server.csv'
local_path= r"C:\Users\....\path"
local_file_name= r"\file_name.csv"

sftp_upload(remote_path, remote_file_name, local_path, local_file_name)
