# from pypims import flood
# import os
# import time

# def timeCount(calcMode, t_start):
#     t_end = time.time()
#     final_time = round((t_end - t_start), 4)
#     print("{0}: {1} s".format(calcMode, final_time))

# if __name__=='__main__':

#     t_start = time.time()
#     path=r'001_floodsim/output/hipims_case'

#     ngpus = 1
#     case_folder = path
#     print(case_folder)

#     if ngpus > 1:
#         flood.run_mgpus(case_folder)
#     else:
#         flood.run(case_folder)

#     print('finished')
#     timeCount('', t_start)

def generate_timeseries(order, d, interval):
    timeseries = {}
    current_time = 0
    for key in order:
        value = d[key]
        for _ in range(value):
            timeseries[current_time] = key
            current_time += interval
    return timeseries

d = {-1: 4, 3000: 11, 2000: 0, 1000: 0, 500: 2}
order = [500, 1000, 2000, 3000, -1]
timeseries = generate_timeseries(order, d, 450)
print(timeseries)




