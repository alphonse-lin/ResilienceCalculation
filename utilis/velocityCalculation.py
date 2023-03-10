from osgeo import gdal
import numpy as np
import os
import rasterio

import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
# __file__获取执行文件相对路径，整行为取上一级的上一级目录
sys.path.append(BASE_DIR)
from utilis.general import timeCount, mkdir
from utilis.plot import show, save

def getGeoTransform(extent, nlines, ncols):
    resx = (extent[2] - extent[0]) / ncols
    resy = (extent[3] - extent[1]) / nlines
    return [extent[0], resx, 0, extent[3] , 0, -resy]

def exportasc(arr, path):
    with open(path, 'wb') as f:
        np.save(f, arr, allow_pickle=False)

if __name__ == '__main__':
    dem_path=r'data\part_london\part\TQ27ne_DTM_1m.tif'
    hx_path=r'data\output\asc\velocity\hUx_7200.asc'
    hy_path=r'data\output\asc\velocity\hUy_7200.asc'
    output_path=r'data\output\asc\velocity\hU_7200.tif'

    hx_data = np.loadtxt(hx_path, skiprows=6)
    hy_data = np.loadtxt(hy_path, skiprows=6)

    hx_square=np.square(hx_data)
    hy_square=np.square(hy_data)

    h_sum=np.add(hx_square, hy_square)
    h_sum=np.sqrt(h_sum)

    # get projection and geotransform information
    dem_dataset = gdal.Open(dem_path)
    projection = dem_dataset.GetProjection()
    geotransform = dem_dataset.GetGeoTransform()

    # Get GDAL driver GeoTiff
    driver = gdal.GetDriverByName('GTiff')
    
    # Get dimensions
    nlines = h_sum.shape[0]
    ncols = h_sum.shape[1]
    nbands = len(h_sum.shape)
    data_type = gdal.GDT_Int16 # gdal.GDT_Float32
    
    # Create a temp grid
    #options = ['COMPRESS=JPEG', 'JPEG_QUALITY=80', 'TILED=YES']
    grid_data = driver.Create('grid_data', ncols, nlines, 1, data_type)#, options)
    
    # Write data for each bands
    grid_data.GetRasterBand(1).WriteArray(h_sum)
    
    # Setup projection and geo-transform
    grid_data.SetProjection(projection)
    grid_data.SetGeoTransform(geotransform)
    
    # Save the file
    driver.CreateCopy(output_path, grid_data, 0)  
    
    # Close the file
    driver = None
    grid_data = None
    
    # Delete the temp grid
    import os                
    os.remove('grid_data')
    #==================================================================

    # save(h_sum, output_path)

    print("successful")

