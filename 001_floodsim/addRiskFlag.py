import pandas as pd
import os

def risk_assessment(traffic_diff, mediation_diff):
    tra=traffic_diff
    med=mediation_diff
    ratio=med*tra
    if traffic_diff < 0 and mediation_diff > 0:
        return 'Lowest Risk', ratio
    elif traffic_diff < 0 and mediation_diff < 0:
        return 'Low Risk', ratio
    elif traffic_diff > 0 and mediation_diff < 0:
        return 'High Risk', ratio
    elif traffic_diff > 0 and mediation_diff > 0:
        return 'Highest Risk', ratio
    elif traffic_diff == 0:
        return 'No Traffic Flow', 0
    elif mediation_diff == 0 and traffic_diff != 0:
        return 'Flooded', 0
    else:
        return 'No Risk', 0

# 加上风险评估标签
if __name__ == '__main__':
    # 1. 读取CSV数据
    input_dir=r'D:\Code\114_temp\008_CodeCollection\005_java\matsim_preparation\src\main\resources\debug\tq38_london_strategy\static_waittodry\static_waittodry\link\withchoice\debug'
    data = pd.read_csv(os.path.join(input_dir,'sort_sample_7-30-am_data.csv'))

    # 计算交通流量差值
    data['traffic_diff_1-2'] = data['HRS8-9avg'] - data['HRS7-8avg']
    data['traffic_diff_2-3'] = data['HRS9-10avg'] - data['HRS8-9avg']

    # 计算五组中介中心性的差值
    groups = ['-1_M', '500_M', '1000_M', '2000_M', '3000_M']

    for group in groups:
        col_1 = f'{group}_h_0_depth'
        col_2 = f'{group}_h_3600_depth'
        col_3 = f'{group}_h_7200_depth'
        
        data[f'{group}_diff_1-2'] = data[col_2] - data[col_1]
        data[f'{group}_diff_2-3'] = data[col_3] - data[col_2]

    # 为每个时间段和每组中介中心性进行风险评估
    risk_columns = []
    ratio_columns = []
    for group in groups:
        risk_col_1_2 = f'{group}_risk_1-2'
        risk_col_2_3 = f'{group}_risk_2-3'
        ratio_col_1_2 = f'{group}_ratio_1-2'
        ratio_col_2_3 = f'{group}_ratio_2-3'
        
        risk_columns.extend([risk_col_1_2, risk_col_2_3])
        ratio_columns.extend([ratio_col_1_2, ratio_col_2_3])
        
        data[risk_col_1_2], data[ratio_col_1_2] = zip(*data.apply(lambda row: risk_assessment(row['traffic_diff_1-2'], row[f'{group}_diff_1-2']), axis=1))
        data[risk_col_2_3], data[ratio_col_2_3] = zip(*data.apply(lambda row: risk_assessment(row['traffic_diff_2-3'], row[f'{group}_diff_2-3']), axis=1))

    # 计算差值比率
    data.to_csv(os.path.join(input_dir,'processed_data.csv'), index=False)

