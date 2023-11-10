import pandas as pd
import os

# 假设df是你的DataFrame
def calculate_risk_and_ratio_for_pairs(row, gap):
    # 初始化结果列表
    results = []
    gap=int(gap)
    # 遍历所有成对的列
    for i in range(3, 3+gap):
        # debug=input_df.columns[i]
        # print(debug)
        # 计算A的差值
        A = row[i] - row[i-1]
        # 计算B的差值
        # debug_2=input_df.columns[i+17]
        # print(debug_2)
        B = row[i+gap+1] - row[i+gap]
        
        # 根据A和B的差值判断风险等级
        if row[i+gap+1]==0:
            risk_level = 'flooded'
        elif A <= 0 and B <= 0:
            A=0.0001
            risk_level = 'lowest'
        elif A <= 0 and B > 0:
            A=0.0001
            risk_level = 'low risk'
        elif A > 0 and B < 0:
            risk_level = 'high risk'
        elif A > 0 and B > 0:
            risk_level = 'highest risk'
        else:
            risk_level = 'unknown'
        
        # 计算ratio（A与B的乘积）
        ratio = abs(B) * A
        
        # 将结果添加到列表中
        results.append((risk_level, ratio))
    
    # 构建索引
    index_risk_level = [f'risk_level_{i}' for i in range(0, gap)]
    index_ratio = [f'ratio_{i}' for i in range(0, gap)]
    index_combined = [val for pair in zip(index_risk_level, index_ratio) for val in pair]
    
    # 将结果转换为一个Series对象，每个元组变成一个单独的列
    result_series = pd.Series([item for pair in results for item in pair], index=index_combined)
    
    return result_series

# 定义一个函数，用于按新的时间间隔合并列
def resample_dataframe(df, default_time_interval, new_time_interval):
    # 计算需要合并的列数
    columns_to_combine = new_time_interval // default_time_interval
    
    # 合并[3:19]中的列
    new_link_counts = [df.iloc[:, 3 + i*columns_to_combine : 3 + (i+1)*columns_to_combine].sum(axis=1) for i in range((19-3)//columns_to_combine)]
    # print(df.columns[2:26])
    # 从[20:36]中选择对应的列
    selected_cols = [20 + i*columns_to_combine - 1 for i in range((36-20)//columns_to_combine + 1)]
    # print(df.columns[27:43])
    selected_data = df.iloc[:, selected_cols]
    
    # 创建新的 DataFrame
    new_df = pd.DataFrame(new_link_counts).transpose()
    
    # 重命名列以匹配原始时间间隔的列名
    columns_name=df.columns
    new_df.columns = [f'{int(columns_name[2])+(i+1)*new_time_interval}' for i in range(new_df.shape[1])]
    
    # 合并新的 link_count 与选中的数据
    final_df = pd.concat([df.iloc[:,:3], new_df, selected_data.reset_index(drop=True)], axis=1)
    
    return final_df


# 加上风险评估标签
if __name__ == '__main__':
    def_t_i=450
    new_t_i=450
    # 1. 读取CSV数据
    tag_dic={"7:30":"7-30-am", "12:00":"12-00-pm", "16:30":"4-00-pm"}
    # tag_dic={"7:30":"7-30-am", "12:00":"12-00-pm", "16:30":"4-00-pm", "no":"no_event"}
    parent_dir=r'D:\Code\114_temp\008_CodeCollection\005_java\matsim_data_backup\debug\tq38_london_strategy\static_waittodry\static_waittodry\final_output'
    
    for tag in tag_dic.keys():
        tag_name=tag_dic[tag]
        input_dir=os.path.join(parent_dir,tag_name)
        input_df = pd.read_csv(os.path.join(input_dir,f'{tag_name}_450s_dtw_matching.csv'))

        # 将辅助函数应用到每一行，并将结果拼接到原来的DataFrame上
        df_resampled = resample_dataframe(input_df, def_t_i, new_t_i)
        # df_resampled.to_csv(os.path.join(input_dir,'debug_selected_7_30_3600s_link_count+choice.csv'), index=False)
        # df_resampled = pd.read_csv(os.path.join(input_dir,'manual_7_dtw_matching.csv'))

        new_data = df_resampled.apply(calculate_risk_and_ratio_for_pairs, gap=7200/new_t_i, axis=1)
        output_df = pd.concat([df_resampled, new_data], axis=1)
        output_df.to_csv(os.path.join(input_dir,f'{new_t_i}s_{tag_name}_risk_level.csv'), index=False)
        print(f'finished_{tag_name}')