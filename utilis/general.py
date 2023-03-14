# general utilis

import numpy as np
import matplotlib.pyplot as plt
import time
import os


def mkdir(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def timeCount(calcMode, t_start):
    t_end = time.time()
    final_time = round((t_end - t_start), 4)
    print("{0}: {1} s".format(calcMode, final_time))

def show(data):
    plt.figure()
    plt.imshow(data)
    plt.show()


def as_num(x):
    y = '{:.10f}'.format(x)  # .10f 保留10位小数
    return y



if __name__ == '__main__':
    # ncols    269
    # nrows    269
    # xllcorner    0
    # yllcorner    0
    # cellsize    10
    # NODATA_value    -9999

    np.set_printoptions(suppress=True)
    # np.set_printoptions(threshold = np.inf) 

    input='1.38889e-05'
    if ('E' in input or 'e' in input):
        x = as_num(float(input))
        print(x)

    # path=r'data\part_london\extractedLondonDEM_2.tif'
    # output=r'data/part_london/dem.txt'
    # tif2asc(path, output)