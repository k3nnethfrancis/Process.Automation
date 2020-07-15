# The following code will refresh the data connection of an excel workbook
# This is particularly useful if you have an excel file that is connected to a database that you want to use in a python script
# You can execute this code before using the workbook in your script to refresh it and get the latest data
# I call it the poor mans API

import win32com.client                                  # The library we will use to refresh our workbook

xlapp = win32com.client.DispatchEx("Excel.Application") # Starts an instance of Excel

path = r'C:\Users\username\Desktop\PATH\FileName.xlsx   # Update this with your workbooks file path

wb = xlapp.workbooks.open(path)                         # Opens the workbook

wb.RefreshAll()                                         # Refreshes the data connection

xlapp.CalculateUntilAsyncQueriesDone()                  # Holds the program and wait until the refresh has completed before continuing

xlapp.DisplayAlerts = False                             # Stops the dialog box from popping up (without this you will be prompted to save the file when running this code)

wb.Save()                                               # Saves the file (also why we don't need to save the file when the dialoge box pops up)

xlapp.Quit()                                            # Quits the connection
