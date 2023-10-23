import pandas as pd
import glob
import os

# Define a function to extract the number from the file name
def extract_number_from_filename(file_path):
    # Split the path into components and take the last component (file name)
    file_name = file_path.split('\\')[-1]
    
    # Extract the number following 'h_' and before '_depth'
    number = int(file_name.split('_h_')[1].split('_depth')[0])
    
    return number

def merge_files_based_on_value(value):
    dir=r'D:\Code\114_temp\008_CodeCollection\001_python\009_ResilienceCalculation\data\floodsim_20221012\choiceData'
    # Use a wildcard to get all matching files
    temp_files = glob.glob(os.path.join(dir,f"{value}_choiceData_h_*_depth.csv"))
    # Sort the file paths based on the extracted number
    files = sorted(temp_files, key=extract_number_from_filename)
    # If no files found for this value, exit the function
    if not files:
        print(f"No files found for value: {value}")
        return

    # Initialize a main dataframe with the first file
    main_df = pd.read_csv(files[0], index_col=0)
    main_df.reset_index(inplace=True)
    main_df.rename(columns={'index': 'id'}, inplace=True)
    main_df = main_df['id']  # Keep only the 'id' column

    # Loop through the files and merge
    for file in files:
        df = pd.read_csv(file, index_col=0)
        df.reset_index(inplace=True)
        df.rename(columns={'index': 'id'}, inplace=True)
        # Merge based on the 'id' column
        main_df = pd.merge(main_df, df, on='id', how='left')
    main_df.fillna(0,inplace=True)
    # Save the merged dataframe to a new CSV file
    output_filename = f"{value}_merged_output.csv"
    main_df.to_csv(os.path.join(dir, output_filename), index=False)
    print(f"Data merged and saved to {output_filename}")

if __name__ == '__main__':
    values_to_merge = ['500', '1000', '2000', '3000', '-1']
    for value in values_to_merge:
        merge_files_based_on_value(value)

    # dir=r'D:\Code\114_temp\008_CodeCollection\001_python\009_ResilienceCalculation\data\floodsim_20221012\choiceData\mix'
    # filename='_merged_output.csv'
    # for value in values_to_merge:
    #     file_path=os.path.join(dir,f"{value}{filename}")
    #     data=pd.read_csv(file_path, index_col=0)
    #      # 初始化一个空的DataFrame来存放复制后的数据
    #     expanded_data = pd.DataFrame(columns=data.columns)
    #     # 遍历原始数据的每一行
    #     for index, row in data.iterrows():
    #         # 将当前行复制一次，并添加到expanded_data中
    #         # 使用concat而不是逐行的append，这是一个更高效的方法
    #         expanded_data = pd.concat([data, data]).sort_index().reset_index()
    #     # 如果您想要保存这个新的DataFrame，可以使用：
    #     expanded_data.to_csv(os.path.join(dir, f'{value}_dup_choice.csv'), index=False)
    #     print(f"Data merged and saved to {value}_dup_choice.csv")
