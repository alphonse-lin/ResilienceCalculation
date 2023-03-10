import numpy as np
import matplotlib.pyplot as plt
import os
from osgeo import gdal

def readtif(input_path):
    dataset = gdal.Open(input_path)
    band1 = dataset.GetRasterBand(1)
    b1 = band1.ReadAsArray()
    return b1

def show(data):
    plt.figure()
    plt.imshow(data)
    plt.show()

def save(data, path):
    plt.clf()
    plt.imshow(data)
    plt.savefig(path, bbox_inches='tight')

if __name__ == '__main__':
    asc_dir=r'data\output\asc'
    img_dir=r'data\output\image'

    # path=r'data\part_london\part\TQ27ne_DTM_1m.tif'
    # arr=readtif(path)
    # show(arr)

    files=os.listdir(asc_dir)
    plt.figure(figsize=(10,10),dpi=300)

    for file in files:
        if not os.path.isdir(file):
            if "h_" in file and file.endswith('asc'):
                asc_path=os.path.join(asc_dir, file)
                asc_data = np.loadtxt(asc_path, skiprows=6)
                
                file_name=file.split('.')[0]
                output_path=os.path.join(img_dir,file_name+".png")

                save(asc_data, output_path)
                print(file)
    print("successful")
    