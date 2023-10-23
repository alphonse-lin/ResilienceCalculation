import pandas as pd
import random

if __name__ == "__main__":
    event_csv=r'D:\Code\114_temp\008_CodeCollection\005_java\matsim_preparation\src\main\resources\debug\tq38_london\flooded_roads_5400.csv'
    
    df=pd.read_csv(event_csv)
    # 按照score列的值从大到小排序
    df = df.sort_values('depth', ascending=False)

    # 当被淹了之后，每一段路它会有一个时间段，需要去降低速度。
    # 因此我们要求的就是在这个时间段里面，每条路的状态
    # 因为我们现在遵循的是First-Close-First-Reopen，所以每过半小时之后或者每过一小时之后，这条路会重新被打开。
    startclock=36000
    starttime=0
    repairtime=3600
    freespeed_factor=0
    capacity_factor=0
    ids=[]
    starttimes=[]
    freespeeds=[]
    capacitys=[]
    for i, row in df.iterrows():
        # 第一轮变化：察觉被淹了，所以在600s之后，就要开始降低速度了。
        starttime_1=startclock+starttime+random.randint(-600, 600)
        freespeed_1=freespeed_factor
        capacity_1=capacity_factor
        ids.append(int(row['id']))
        starttimes.append(starttime_1)
        freespeeds.append(freespeed_1)
        capacitys.append(capacity_1)

        # 第二轮变化：开始抢修，所以在3000s之后，抢修完成。
        starttime_2=starttime_1+repairtime+row['depth']*1200
        freespeed_2=1
        capacity_2=1
        ids.append(int(row['id']))
        starttimes.append(starttime_2)
        freespeeds.append(freespeed_2)
        capacitys.append(capacity_2)

    # 将flooded_roads输出到一个新的文件
    output_csv=r'D:\Code\114_temp\008_CodeCollection\005_java\matsim_preparation\src\main\resources\debug\networkChange.csv'
    df = pd.DataFrame({'id': ids, 'starttime': starttimes, 'freespeed': freespeeds, 'capacity': capacitys})
    df.to_csv(output_csv, index=False)
    print(output_csv)
    print("finished")
