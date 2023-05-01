import pandas as pd
import os
# read the excel file
#conding=utf8  
 

file_dir=r'D:\OneDrive\Documents\002_UCL\005_PhdPrepared\001_essay\002_Topology_road against flood\001_code\002_output\002_boundaryCentraility'
g = os.walk(file_dir)  

file_paths=[]
for path,dir_list,file_list in g:  
    for file_name in file_list:  
        file_paths.append(os.path.join(path, file_name))

# define file paths for input and output
output_file = r'D:\OneDrive\Documents\002_UCL\005_PhdPrepared\001_essay\002_Topology_road against flood\001_code\002_output\002_boundaryCentraility\output.xlsx'  # replace with your desired output file path

# define sheet name to extract
sheet_name = 'Sheet0'

# create an empty dictionary to hold the merged dataframes
merged_data = {}

# loop over each file path and extract the sheet data
for file_path in file_paths:
    # read the excel file and extract the specified sheet
    sheet_data = pd.read_excel(file_path, sheet_name=sheet_name, header=0)
    
    # extract the file name without extension
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    
    # add the sheet data to the merged_data dictionary, with the key being the file name
    merged_data[file_name] = sheet_data
    
# create a new Excel writer object
writer = pd.ExcelWriter(output_file, engine='xlsxwriter')

# loop over each key-value pair in the merged_data dictionary and write each value to a separate sheet in the new Excel file
for key, value in merged_data.items():
    value.to_excel(writer, sheet_name=key, index=False)

# save the new Excel file
writer.save()