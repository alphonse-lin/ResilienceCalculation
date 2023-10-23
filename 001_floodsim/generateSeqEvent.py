import pandas as pd
import random
import numpy as np
import geopandas as gpd
from collections import defaultdict

import os
#TODO：需要更正repairtime的问题

# 生成组合的时间序列
def generate_timeseries(order, d, interval):
    timeseries = {}
    current_time = 0
    for key in order:
        value = d[key]
        for _ in range(value):
            timeseries[current_time] = key
            current_time += interval
    return timeseries

# 生成各类组合
def combinations(remaining, categories):
    # 如果没有剩余的数量，返回一个空的字典
    if remaining == 0:
        return [defaultdict(int)]
    
    # 如果没有剩余的类别或者剩余的数量小于0，返回空列表
    if not categories or remaining < 0:
        return []
    
    results = []
    for i in range(remaining + 1):
        # 选择当前类别的i个，递归处理剩下的类别
        for comb in combinations(remaining - i, categories[1:]):
            # 创建一个新的字典，包括当前类别的选择
            new_comb = defaultdict(int, comb)
            new_comb[categories[0]] += i
            results.append(new_comb)
            
    return results

# 一遇到水，先关了，等雨停了，再逐步打开
# First Close First Open
def StaticSimulate_WaitToDry(flag_df, depth_df, startclock, repairtime, buffertime, freespeed_factor, capacity_factor, event_dir):
    ids=[]
    starttimes=[]
    freespeeds=[]
    capacitys=[]
    
    for i, row in flag_df.iterrows():
        # 第一轮变化：察觉被淹了，所以在600s之后，就要开始降低速度了。
        
        flag=row[1:]> 0
        if (flag).any():
            # print(row)
            row_depth=depth_df[depth_df['id']==row['id']].values[0]
            flag_depth=row_depth[1:]>3
            if flag_depth.any():
                starttime = int(depth_df.columns[(flag_depth).argmax()+1].split('_')[1])
                # last_positive_index = np.where(flag)[0][-1]
                # end_att = flag_df.columns[last_positive_index+1]
                # end_time = int(end_att.split('_')[1])

                # starttime_1=startclock+starttime+random.randint(-600, 600)
                starttime_1=startclock+starttime
                freespeed_1=freespeed_factor
                capacity_1=capacity_factor
                ids.append(int(row['id']))
                starttimes.append(starttime_1)
                freespeeds.append(freespeed_1)
                capacitys.append(capacity_1)

                # 第二轮变化：一个小时后，不下雨了，看看水深如何，如果水深小雨0.3m，就开始行车，否则继续等待。
                # starttime_2=round(startclock+end_time+depth_df.iloc[i][f"{end_att}_depth"]*repairtime)
                # starttime_2=round(startclock+end_time)
                starttime_2=round(starttime_1 + 3600)
                
                if starttime+3600 <=7200 :
                    depth=depth_df.iloc[i][f"h_{starttime+3600}_depth"]
                    if depth <=3:
                        starttime_2=round(starttime_1 + 3600)
                        freespeed_2=0.5
                        capacity_2=0.5
                    else:
                        starttime_2=round(starttime_1 + 3600 + depth/0.002)
                        freespeed_2=0
                        capacity_2=0
                else:
                    depth=depth_df.iloc[i][f"h_7200_depth"]
                    if depth<=3:
                        starttime_2=round(starttime_1 + 3600)
                        freespeed_2=0.5
                        capacity_2=0.5
                    else:
                        starttime_2=round(starttime_1 + 3600 + depth/0.004)
                        freespeed_2=0
                        capacity_2=0
                ids.append(int(row['id']))
                starttimes.append(starttime_2)
                freespeeds.append(freespeed_2)
                capacitys.append(capacity_2)

                # 第三轮变化：变成1
                # starttime_3=starttime_2+random.randint(buffertime/2, buffertime)
                starttime_3=starttime_2+buffertime
                freespeed_3=1
                capacity_3=1
                
                ids.append(int(row['id']))
                starttimes.append(starttime_3)
                freespeeds.append(freespeed_3)
                capacitys.append(capacity_3)
    return ids, starttimes, freespeeds, capacitys

# 一遇到水，先关了，等雨停了，再逐步打开
# First Close First Open
def StaticSimulate_FCFO(flag_df, depth_df, startclock, repairtime, buffertime, freespeed_factor, capacity_factor, event_dir):
    ids=[]
    starttimes=[]
    freespeeds=[]
    capacitys=[]
    
    for i, row in flag_df.iterrows():
        # 第一轮变化：察觉被淹了，所以在600s之后，就要开始降低速度了。
        
        flag=row[1:]> 0
        if (flag).any():
            # print(row)
            row_depth=depth_df[depth_df['id']==row['id']].values[0]
            flag_depth=row_depth[1:]>3
            if flag_depth.any():
                starttime = int(depth_df.columns[(flag_depth).argmax()+1].split('_')[1])
                # last_positive_index = np.where(flag)[0][-1]
                # end_att = flag_df.columns[last_positive_index+1]
                # end_time = int(end_att.split('_')[1])

                # starttime_1=startclock+starttime+random.randint(-600, 600)
                starttime_1=startclock+starttime
                freespeed_1=freespeed_factor
                capacity_1=capacity_factor
                ids.append(int(row['id']))
                starttimes.append(starttime_1)
                freespeeds.append(freespeed_1)
                capacitys.append(capacity_1)

                # 第二轮变化：开始抢修，所以在1200s之后，抢修完成。
                # starttime_2=round(startclock+end_time+depth_df.iloc[i][f"{end_att}_depth"]*repairtime)
                # starttime_2=round(startclock+end_time)
                starttime_2=round(starttime_1 + 3600)
                freespeed_2=0.5
                capacity_2=0.5
                ids.append(int(row['id']))
                starttimes.append(starttime_2)
                freespeeds.append(freespeed_2)
                capacitys.append(capacity_2)

                # 第三轮变化：变成1
                # starttime_3=starttime_2+random.randint(buffertime/2, buffertime)
                starttime_3=starttime_2+buffertime
                freespeed_3=1
                capacity_3=1
                
                ids.append(int(row['id']))
                starttimes.append(starttime_3)
                freespeeds.append(freespeed_3)
                capacitys.append(capacity_3)
    return ids, starttimes, freespeeds, capacitys

# Open Based On Importance
def StaticSimulate_1(flag_df, depth_df, score_df, startclock, repairtime, buffertime, freespeed_factor, capacity_factor, event_dir):
    ids=[]
    starttimes=[]
    freespeeds=[]
    capacitys=[]
    
    for i, row in flag_df.iterrows():
        # 第一轮变化：察觉被淹了，所以在600s之后，就要开始降低速度了。
        
        flag=row[1:]> 0
        if (flag).any():
            # print(row)
            row_depth=depth_df[depth_df['id']==row['id']].values[0]
            flag_depth=row_depth[1:]>3
            if flag_depth.any():
                starttime = int(depth_df.columns[(flag_depth).argmax()+1].split('_')[1])
                # starttime = int(flag_df.columns[(flag).argmax()+1].split('_')[1])
                # last_positive_index = np.where(flag)[0][-1]
                # end_att = flag_df.columns[last_positive_index+1]
                # end_time = int(end_att.split('_')[1])

                # starttime_1=startclock+starttime+random.randint(-600, 600)
                starttime_1=startclock+starttime
                freespeed_1=freespeed_factor
                capacity_1=capacity_factor
                ids.append(int(row['id']))
                starttimes.append(starttime_1)
                freespeeds.append(freespeed_1)
                capacitys.append(capacity_1)

                # 第二轮变化：开始抢修，所以在1200s之后，抢修完成。
                # starttime_2=round(startclock+end_time+depth_df.iloc[i][f"{end_att}_depth"]*repairtime)
                # starttime_2=round(startclock+end_time)
                score=score_df.loc[score_df['id']==int(row['id']), 'm_ch_500'].values[0]
                score = 0.01 if score ==0 else score
                starttime_2=round(starttime_1+min((1/score)*repairtime, 7200))
                freespeed_2=0.5
                capacity_2=0.5
                ids.append(int(row['id']))
                starttimes.append(starttime_2)
                freespeeds.append(freespeed_2)
                capacitys.append(capacity_2)

                # 第三轮变化：变成1
                # starttime_3=starttime_2+random.randint(buffertime/2, buffertime)
                starttime_3=starttime_2+buffertime
                freespeed_3=1
                capacity_3=1
                
                ids.append(int(row['id']))
                starttimes.append(starttime_3)
                freespeeds.append(freespeed_3)
                capacitys.append(capacity_3)
            else:
                continue
    return ids, starttimes, freespeeds, capacitys

# Open Based On Dynamic Importance
def DynamicSimulate(timeseries, flag_df, depth_df, score_df, startclock, repairtime, buffertime, freespeed_factor, capacity_factor, event_dir):
    ids=[]
    starttimes=[]
    freespeeds=[]
    capacitys=[]
    
    for i, row in flag_df.iterrows():
        # 第一轮变化：察觉被淹了，所以在600s之后，就要开始降低速度了。
        flag=row[1:]> 0
        if (flag).any():
            # print(row)
            row_depth=depth_df[depth_df['id']==row['id']].values[0]
            flag_depth=row_depth[1:]>3
            if flag_depth.any():
                starttime = int(depth_df.columns[(flag_depth).argmax()+1].split('_')[1])
                # last_positive_index = np.where(flag)[0][-1]
                # end_att = flag_df.columns[last_positive_index+1]
                # end_time = int(end_att.split('_')[1])

                starttime_1=startclock+starttime
                freespeed_1=freespeed_factor
                capacity_1=capacity_factor
                ids.append(int(row['id']))
                starttimes.append(starttime_1)
                freespeeds.append(freespeed_1)
                capacitys.append(capacity_1)

                # 第二轮变化：开始抢修，所以在1200s之后，抢修完成。
                # print(score_df.loc[score_df['id']==int(row['id'])])
                # 0, 450, 900, 1350, 1800, 2250, 2700, 3150, 3600, 4050, 4500, 4950, 5400, 5850, 6300, 6750, 7200
                # 500, 500, 500, 500, 500, 1000, 1000, 1000, 1000, 2000, 2000, 2000, 2000, 3000, 3000, 3000, 3000
                index_value=timeseries[starttime]
                score=score_df.loc[score_df['id']==int(row['id']), f'm_ch_{index_value}'].values[0]
                score = 0.01 if score ==0 else score

                starttime_2=round(starttime_1+min((1/score)*repairtime, 7200))
                # starttime_2=round(startclock+end_time)
                # print(road_network.loc[road_network['id']==int(row['id']), 'freespeed'])
                freespeed_2=0.5
                capacity_2=0.5
                ids.append(int(row['id']))
                starttimes.append(starttime_2)
                freespeeds.append(freespeed_2)
                capacitys.append(capacity_2)

                # 第三轮变化：变成1
                starttime_3=starttime_2+random.randint(buffertime/2, buffertime)
                freespeed_3=1
                capacity_3=1
                
                ids.append(int(row['id']))
                starttimes.append(starttime_3)
                freespeeds.append(freespeed_3)
                capacitys.append(capacity_3)
    return ids, starttimes, freespeeds, capacitys

def Export(ids, starttimes, freespeeds, capacitys, base_dir, folder_name, combination_name):
    # 将flooded_roads输出到一个新的文件
    output_csv=os.path.join(base_dir,folder_name,'eventCSV', f'sequenced_networkChange_{combination_name}.csv')
    df = pd.DataFrame({'id': ids, 'starttime': starttimes, 'freespeed': freespeeds, 'capacity': capacitys})
    df.to_csv(output_csv, index=False)
    print(output_csv)

def ExportSingle(ids, starttimes, freespeeds, capacitys, base_dir, folder_name):
    # 将flooded_roads输出到一个新的文件
    output_csv=os.path.join(base_dir,folder_name, f'sequenced_networkChange.csv')
    df = pd.DataFrame({'id': ids, 'starttime': starttimes, 'freespeed': freespeeds, 'capacity': capacitys})
    df.to_csv(output_csv, index=False)
    print(output_csv)

if __name__ == "__main__":
    # 第三步：生成连续道路调控事件
    base_dir=r'D:\Code\114_temp\008_CodeCollection\005_java\matsim_preparation\src\main\resources\debug\tq38_london_strategy'
    # road_data_path=os.path.join(base_dir, 'network_transfer.geojson')
    # road_network = gpd.read_file(road_data_path)

    flag_csv=os.path.join(base_dir,'002_event', 'flag_sequenced_flooded_roads.csv')
    depth_csv=os.path.join(base_dir,'002_event','depth_sequenced_flooded_roads.csv')
    score_csv=os.path.join(base_dir, 'network_importance_final.csv')
    flag_df=pd.read_csv(flag_csv)
    depth_df=pd.read_csv(depth_csv)
    score_df=pd.read_csv(score_csv)

    # 当被淹了之后，每一段路它会有一个时间段，需要去降低速度。
    # 因此我们要求的就是在这个时间段里面，每条路的状态
    # 因为我们现在遵循的是First-Close-First-Reopen，所以每过半小时之后或者每过一小时之后，这条路会重新被打开。
    startclock=57600
    repairtime=300
    buffertime=300
    freespeed_factor=0
    capacity_factor=0

#region 静态调控
    ids, starttimes, freespeeds, capacitys=StaticSimulate_WaitToDry(flag_df, depth_df, startclock, repairtime, buffertime, freespeed_factor, capacity_factor, base_dir)
    ExportSingle(ids, starttimes, freespeeds, capacitys, base_dir, 'static_waittodry')

    # ids, starttimes, freespeeds, capacitys=StaticSimulate_FCFO(flag_df, depth_df, startclock, repairtime, buffertime, freespeed_factor, capacity_factor, base_dir)
    # ExportSingle(ids, starttimes, freespeeds, capacitys, base_dir, 'static_fcfo')

    # ids, starttimes, freespeeds, capacitys=StaticSimulate_1(flag_df, depth_df, score_df, startclock, repairtime, buffertime, freespeed_factor, capacity_factor, base_dir)
    # ExportSingle(ids, starttimes, freespeeds, capacitys, base_dir, 'static_1')
#endregion

#region 动态调控
    # categories = [500, 1000, 2000, 3000, -1]
    # combs = combinations(17, categories)
    # sampled_combs = random.sample(combs, 100)
    # sampled_combs.append({500: 17, 1000: 0, 2000: 0, 3000: 0, -1: 0})
    # sampled_combs.append({500: 0, 1000: 17, 2000: 0, 3000: 0, -1: 0})
    # sampled_combs.append({500: 0, 1000: 0, 2000: 17, 3000: 0, -1: 0})
    # sampled_combs.append({500: 0, 1000: 0, 2000: 0, 3000: 17, -1: 0})
    # sampled_combs.append({500: 0, 1000: 0, 2000: 0, 3000: 0, -1: 17})
    # # 从列表中随机选择200个元素
    
    # for comb in sampled_combs:
    #     d = comb
    #     str_d = "_".join([f"{k}_{v}" for k, v in d.items()])
    #     order = [500, 1000, 2000, 3000, -1]
    #     timeseries = generate_timeseries(order, d, 450)
    #     ids, starttimes, freespeeds, capacitys=DynamicSimulate(timeseries, flag_df, depth_df, score_df, startclock, repairtime, buffertime, freespeed_factor, capacity_factor, base_dir)
    #     Export(ids, starttimes, freespeeds, capacitys, base_dir, 'dynamic_12_00_pm', str_d)
#endregion