import pandas as pd
import os
from sklearn.preprocessing import MinMaxScaler

if __name__ == '__main__':
    # 组合matsim和choice的数据
    # Step 1: Load the data
    input_dir=r'D:\Code\114_temp\008_CodeCollection\005_java\matsim_preparation\src\main\resources\debug\tq38_london_strategy\static_waittodry\static_waittodry\link'
    output_dir=os.path.join(input_dir,'withchoice')
    file_name=r'12-00-pm_linkstats.csv'
    file_nick_name=file_name.split('_')[0]
    excel_data = pd.read_csv(os.path.join(input_dir,file_name))

    choice_dir=r'D:\Code\114_temp\008_CodeCollection\001_python\009_ResilienceCalculation\data\floodsim_20221012\choiceData\mix'
    choice_files=os.listdir(choice_dir)
    choice_files.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    csv_data_list=[]
    for file in choice_files:
        tag=file.split('_')[0]
        temp_df=pd.read_csv(os.path.join(choice_dir, file))[['id',
                                                            'M_h_0_depth', 'M_h_450_depth','M_h_900_depth', 'M_h_1350_depth',
                                                            'M_h_1800_depth', 'M_h_2250_depth','M_h_2700_depth','M_h_3150_depth','M_h_3600_depth',
                                                            'M_h_4050_depth', 'M_h_4500_depth','M_h_4950_depth', 'M_h_5400_depth',
                                                            'M_h_5850_depth', 'M_h_6300_depth','M_h_6750_depth','M_h_7200_depth']]
        csv_data = temp_df.add_prefix(f'{tag}_')
        # Rename the 'id' column to remove the label prefix
        csv_data = csv_data.rename(columns={f'{tag}_id': 'id'})
        # Select columns to scale (excluding 'id')
        # Initialize a scaler
        scaler = MinMaxScaler() 
        columns_to_scale = [col for col in csv_data.columns if col != 'id']
        # Apply the scaler
        csv_data[columns_to_scale] = scaler.fit_transform(csv_data[columns_to_scale])
        # 2. 重复第二份数据
        csv_data_duplicated = pd.concat([csv_data, csv_data]).sort_index().reset_index(drop=True)
        # csv_data_duplicated.to_csv(os.path.join(output_dir,f'{file_nick_name}_dup_choice.csv'), index=False)
        csv_data_list.append(csv_data_duplicated)

    # Step 2: Process the LINK column
    # excel_data['LINK_id'] = (excel_data['LINK'] / 2).astype(int)  # Dividing by 2 and converting to integer

    # Step 3: Merge the data
    merged_data = excel_data
    for i, csv_data in enumerate(csv_data_list):
        csv_data_2 = csv_data.drop(columns=['id'])
        # merged_data = pd.merge(merged_data, csv_data, left_on='LINK_id', right_on='id', how='left',suffixes=('', f'_tmp{i}'))
        merged_data = pd.concat([merged_data, csv_data_2], axis=1)
    # Remove all columns that end with '_tmp' followed by a number
    merged_data = merged_data.drop(columns=[col for col in merged_data.columns if col.endswith(tuple([f'_tmp{i}' for i in range(len(csv_data_list))]))])
    # merged_data = merged_data.drop(columns=['LINK_id'])

    merged_data.to_csv(os.path.join(output_dir,f'{file_nick_name}_merged_output.csv'), index=False)
    print(f'{file_name} finished')
