import pandas as pd
import os

if __name__ == '__main__':
    # 第六步：对于输出的count_excel进行整合
    input_dir=r'D:\Code\114_temp\008_CodeCollection\005_java\matsim_preparation\src\main\resources\debug\tq38_london_strategy\static_waittodry\static_waittodry\4-00-pm'

    ls=os.listdir(input_dir)
    files=[]
    for file in ls:
        if 'output_events' in file and '.xlsx' in file:
            files.append(file)
    files.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))

    main_df = pd.read_excel(os.path.join(input_dir,'output_events_0.xlsx'))
    main_df = main_df[['link_id']]  # Keep only the link_id column

    for file in files:
        file_name = file
        print(file_name)
        df = pd.read_excel(os.path.join(input_dir,file_name))
        index=file.split('_')[2].split('.')[0]
        # Rename the count column
        df = df.rename(columns={'count': f'count_{index}'})
        
        # Merge with main dataframe based on link_id
        main_df = pd.merge(main_df, df[['link_id', f'count_{index}']], on='link_id', how='outer')
    main_df.fillna(0,inplace=True)
    main_df.sort_values(by=['link_id'],inplace=True)
    main_df.to_csv(os.path.join(input_dir,'merged_output.csv'), index=False)
        

    # # Initialize a main dataframe with the first file
    # main_df = pd.read_excel('output_events_0.xlsx')

    # main_df = main_df[['link_id']]  # Keep only the link_id column

    # # Loop through the files
    # for i in range(30):  # Assuming there are 30 files as mentioned
    #     file_name = f'output_events_{i}.xlsx'
    #     df = pd.read_excel(file_name)
        
    #     # Rename the count column
    #     df = df.rename(columns={'count': f'count_{i}'})
        
    #     # Merge with main dataframe based on link_id
    #     main_df = pd.merge(main_df, df[['link_id', f'count_{i}']], on='link_id', how='left')

    # # Save the merged dataframe to a new CSV file
    # main_df.to_csv('merged_output.csv', index=False)
