import pandas as pd
import os

input_dir=r'D:\Code\114_temp\008_CodeCollection\005_java\matsim_preparation\src\main\resources\debug\tq38_london_strategy\static_waittodry\static_waittodry\link\withchoice'
file_flooded='7-30-am_merged_output.csv'
file_dry='no_merged_output.csv'

flooded_data = pd.read_csv(os.path.join(input_dir,file_flooded))
dry_data = pd.read_csv(os.path.join(input_dir,file_dry))

# 确保两个DataFrame的维度是一样的
if flooded_data.shape != dry_data.shape:
    raise ValueError("两个CSV文件的维度不一样!")

# 对除了第一列和第二列的其他列进行减法操作
for col in flooded_data.columns[1:]:
    flooded_data[col] = flooded_data[col] - dry_data[col]

# 保存到新的CSV文件
flooded_data.to_csv(os.path.join(input_dir,'result.csv'), index=False)