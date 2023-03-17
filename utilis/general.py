# general utilis

from osgeo import gdal
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

def tif2asc(path, output):
    ds=gdal.Open(path)
    # gt=ds.GetGeoTransform()
    # proj=ds.GetProjection()
    # print(gt)
    # print(proj)

    band=ds.GetRasterBand(1)
    array=band.ReadAsArray()
    array=array-array.min()
    np.savetxt(output, array, delimiter=' ',fmt='%.1f')

    with open(output, 'r+') as f:
        content = f.read()        
        f.seek(0, 0)
        f.write('nclos\t'+input(array.shape[0])+"\n")
        f.write('nrows\t'+input(array.shape[1])+"\n")
        f.write('xllcorner\t'+"0"+"\n")
        f.write('yllcorner\t'+"0"+"\n")
        f.write('cellsize\t'+"10"+"\n")
        f.write('cellsize\t'+"-9999"+"\n")
        f.write(content)

    print("successful")

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
    