#!python

# REFRESH THE DATA CONNECTION IN THE EXCEL WORKBOOK

# Import Packages

import win32com.client                                   # For working with excel files and refreshing the connection

def refresh_excel(file_path):
    '''
    Takes a file path of an excel workbook and refreshes any data connections.
        Parameters:
                file_path: full path of excel file to be refreshed
        Returns:
            None.
        Notes:
            Only works with excel files.
    '''
    xl = win32com.client.DispatchEx("Excel.Application")  # Start an instance of Excel

    wb = xl.workbooks.Open(file_path)                     # Open the workbook

    wb.RefreshAll()                                       # Refresh all data connections in said workbook

    xl.CalculateUntilAsyncQueriesDone()                   # Holds the program until the refresh has completed

    xl.DisplayAlerts = False                              # Stops the dialog box from popping up

    wb.Save()                                             # Saves the file

    wb.Close()                                            # Closes the workbook
    xl.Quit()                                             # Quits the connection

    del wb                                                # Optional - use these when you are scheduling this program to run
    del xl
    return                                                # They terminate Excel in the background (Task Manager) which ensures a proper refresh
