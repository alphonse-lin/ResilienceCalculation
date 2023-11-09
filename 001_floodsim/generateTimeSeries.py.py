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




