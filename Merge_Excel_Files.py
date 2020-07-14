# Merge Multiple Excel Files into one with Append

# Import pandas for data manipulation
import pandas as pd

# Read all three files into pandas dataframes
# Your files path goes in the brackets

File1 = pd.read_excel(r'C:\Users\username\Desktop\Folder\FileName.xlsx')
File2 = pd.read_excel(r'C:\Users\username\Desktop\Folder\FileName.xlsx')
File3 = pd.read_excel(r'C:\Users\username\Desktop\Folder\FileName.xlsx')

# Create a list of the files in order you want them appended
all_df_list = [File1,File2,File3]

# Merge all dataframes in all_df_list
# Pandas will automatically append based on similar column names
appended_df = pd.concat(all_df_list)

# Write the appended dataframe to an excel file
# Add index=False parameter to not include row numbers
# Change the path to where you want the file saved
# NewFileName.xlxs is the new files name
appended_df.to_excel(r'C:\Users\username\Desktop\Folder\NewFileName.xlsx', index=False)
