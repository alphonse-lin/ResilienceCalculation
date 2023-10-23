import pandas as pd
import os

dir=r'D:\Code\114_temp\008_CodeCollection\005_java\matsim_preparation\target\classes\debug\tq38_london_strategy\002_event'
# 读取csv文件
df = pd.read_csv(os.path.join(dir, "depth_sequenced_flooded_roads.csv"))

# 选择偶数行 (注意：行索引从0开始，所以实际的偶数行对应于奇数索引)
even_rows = df.iloc[1::2]

# 保存到新的csv文件
even_rows.to_csv(os.path.join(dir, 'output_even_rows.csv'), index=False)
