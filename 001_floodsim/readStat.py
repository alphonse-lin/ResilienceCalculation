import gzip
import pandas as pd
import os

# Read the linkstats.txt.gz file
if __name__ == '__main__':
    name_list=['4-00-pm', '7-30-am', '12-00-pm', 'no_event']
    input_dir=r'D:/Code/114_temp/008_CodeCollection/005_java/matsim_preparation/src/main/resources/debug/tq38_london_strategy/static_waittodry/static_waittodry'
    output_dir=r'D:\Code\114_temp\008_CodeCollection\005_java\matsim_preparation\src\main\resources\debug\tq38_london_strategy\static_waittodry\static_waittodry'
    for name in name_list:
        path=os.path.join(input_dir, f'output_{name}/ITERS/it.20')
        with gzip.open(os.path.join(path,'20.linkstats.txt.gz')) as f:
            data = pd.read_csv(f'',delimiter='\t')

        hrs_avg_columns = data.filter(regex='HRS.*avg')
        link_column = data[['LINK']]
        selected_data = pd.concat([link_column, hrs_avg_columns], axis=1)
        selected_data_without_last_column = selected_data.iloc[:, :-1]
        selected_data_without_last_column.sort_values(by=['LINK'], inplace=True)
        selected_data_without_last_column.to_csv(os.path.join(output_dir,f'{name}_linkstats.csv'),index=False)
        print(f'{name} finished')
