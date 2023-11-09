import datetime
import numpy as np

def sec2Time(start_time,s):
    delta = datetime.timedelta(seconds=s)
    start_time += delta

    # 将结果格式化为时间字符串，只包含小时和分钟
    time_str = start_time.strftime('%H:%M')
    return time_str

# Extra: Convert seconds to time
if __name__ == '__main__':
    # 初始时间的年月日设置为2022年1月1日
    start_time = datetime.datetime(2022, 1, 1, 16, 00)

    # 秒数列表
    times = [0, 450, 900, 1350, 1800, 2250, 2700, 3150, 3600, 4050, 4500, 4950, 5400, 5850, 6300, 6750, 7200]
    dict = {500:0,1000:8,2000:0,3000:3,-1:6}

    res = []
    counter = 0
    for key, value in dict.items():
        if value != 0:
            if counter == 0:
                s_time = times[counter]
            else:
                s_time = times[counter-1]
            s_time=sec2Time(start_time,s_time)
            e_time = times[counter + value - 1]
            e_time=sec2Time(start_time,e_time)
            res.append(f"{s_time}-{e_time} {key}m")
            counter += value

    res_str = '\n'.join(res)
    print(res_str)



