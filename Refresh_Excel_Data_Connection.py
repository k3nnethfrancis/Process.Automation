# The following code will refresh the data connection of an excel workbook
# This is particularly useful if you have an excel file that is connected to a database that you want to use in a python script
# You can execute this code before using the workbook in your script to refresh it and get the latest data
# I call it the poor mans API

import win32com.client as win32                         # The library we will use to refresh our workbook

xl = win32.client.DispatchEx('Excel.Application')       # Starts an instance of Excel

path = r'C:\Users\username\Desktop\PATH\FileName.xlsx'  # Update this with your workbooks file path

wb = xl.workbooks.Open(path)                            # Opens the workbook

wb.RefreshAll()                                         # Refreshes the data connection

xl.CalculateUntilAsyncQueriesDone()                     # Holds the program and wait until the refresh has completed before continuing

xl.DisplayAlerts = False                                # Stops the dialog box from popping up

wb.Save()                                               # Saves the file

wb.Close()                                              # Closes the workbook

xl.Quit()                                               # Quits the connection
# del wb                                                # Excel sometimes stays running in the background
# del xl                                                # Deleting these variables seems to solve that problem
                                                        # You will want to uncomment these 2 lines if you are scheduling this program to run
