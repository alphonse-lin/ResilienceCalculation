from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
import numpy as np
import pandas as pd
import os
from collections import Counter

if __name__ == '__main__':
    # 第七步：对于输出的count_excel进行整合,然后用dtw进行pattern匹配
    input_dir=r'D:\Code\114_temp\008_CodeCollection\005_java\matsim_preparation\src\main\resources\debug\tq38_london_strategy\static_waittodry\static_waittodry\link\withchoice'

    # 读取csv文件
    file_name='7-30-am_merged_output.csv'
    data = pd.read_csv(os.path.join(input_dir,file_name))

    results = []
    result_dic={}

# 循环遍历每一行数据
idx_list=[]
match_list=[]
best_sequences_df = pd.DataFrame()
for row_index in range(data.shape[0]):
    # 获取当前行的参考序列和待匹配的序列
    reference_sequence = data.iloc[row_index, [8, 9, 10]].values

    sequences_indices = [
        list(range(25, 42,8)),
        list(range(42, 59,8)),
        list(range(59, 76,8)),
        list(range(76, 93,8)),
        list(range(93, 110,8))
    ]

    # # # 打印对应的列名
    # for indices in sequences_indices:
    #     print(data.columns[indices].tolist())

    sequences = [data.iloc[row_index, indices].values for indices in sequences_indices]

    min_distance = float('inf')
    best_match_index = -1
    best_sequence = None

    for idx, seq in enumerate(sequences):
        distance, _ = fastdtw(reference_sequence, seq, dist=euclidean)
        if distance < min_distance:
            min_distance = distance
            best_match_index = idx
            best_sequence = seq
    
    # # results.append((row_index, best_match_index, min_distance))
    # if best_match not in result_dic.keys():
    #     result_dic[best_match_index]=[]
    #     result_dic[best_match_index].append(row_index)
    # else:
    #     result_dic[best_match_index].append(row_index)

    idx_list.append(data.iloc[row_index]['LINK'])
    match_list.append(best_match_index)
    # 将最佳匹配序列转为DataFrame，并转置（因为我们希望每一个序列元素成为一个列）
    temp_df = pd.DataFrame(best_sequence).T
    best_sequences_df = pd.concat([best_sequences_df, temp_df], ignore_index=True)



# 创建一个DataFrame来存放idx和match_idx
export_data = pd.DataFrame({
    'LINK': idx_list,
    'match_idx': match_list
})

# 将idx/match_idx的DataFrame和best_sequences_df拼接
final_export_data = pd.concat([export_data, best_sequences_df], axis=1)

final_export_data.to_csv(os.path.join(input_dir,f"{file_name.split('_')[0]}_selected_data_3points.csv"), index=False)
print(f'{file_name}_finished')

# for i in result_dic.keys():
#       print(i, ":", len(result_dic[i]))

# print(f"对于行{row_index}，与第1份数据最匹配的是第{best_match}份数据，DTW距离为: {distance}")
