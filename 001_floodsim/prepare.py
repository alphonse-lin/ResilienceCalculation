import sys
import numpy as np
from osgeo import gdal

def generateDEM(ds, output):
    band=ds.GetRasterBand(1)
    array=band.ReadAsArray()
    array=array-array.min()
    np.savetxt(output, array, delimiter=' ',fmt='%.1f')

    with open(output, 'r+') as f:
        content = f.read()        
        f.seek(0, 0)
        f.write('nclos\t'+str(array.shape[0])+"\n")
        f.write('nrows\t'+str(array.shape[1])+"\n")
        f.write('xllcorner\t'+"0"+"\n")
        f.write('yllcorner\t'+"0"+"\n")
        f.write('cellsize\t'+"10"+"\n")
        f.write('cellsize\t'+"-9999"+"\n")
        f.write(content)

    print("successful")

def generateRainFall(inDs, output_path):
    gt=inDs.GetGeoTransform()
    proj=inDs.GetProjection()
    rows = inDs.RasterYSize
    cols = inDs.RasterXSize

    # create the output image
    driver = gdal.GetDriverByName('GTiff')
    #print driver
    outDs = driver.Create(output_path, cols, rows, 1, gdal.GDT_Int32)

    if outDs is None:
        print ('create failed')
        sys.exit(1)

    outBand = outDs.GetRasterBand(1)
    outData = np.zeros((rows,cols), np.int16)


    for i in range(0, rows):
        for j in range(0, cols):
            outData[i,j] = 0

            # write the data
    outBand.WriteArray(outData, 0, 0)

    # flush data to disk, set the NoData value and calculate stats
    outBand.FlushCache()
    outBand.SetNoDataValue(-9999)

    # georeference the image and set the projection
    outDs.SetGeoTransform(gt)
    outDs.SetProjection(proj)

    del outData

def arregateDEM(building_path, dem_path):
    pass

def generateLandCover():
    pass

if __name__ == '__main__':
    np.set_printoptions(suppress=True)
    # # np.set_printoptions(threshold = np.inf) 

    # path=r'data\part_london\extractedLondonDEM_2.tif'
    # dem_output=r'data/part_london/dem.txt'
    # rainfall_output=r'data/part_london/rainfall.txt'
    
    # # ds=gdal.Open(path)

    # # generateDEM(ds, dem_output)
    # # generateRaster(ds, rainfall_output)

    building_path=r'data\part_london\tq38sw_2m\building.asc'
    dtm_path=r'data\part_london\tq38sw_2m\dtm.asc'
    dem_path=r'data\part_london\tq38sw_2m\dem.tif'
    rainfall_path=r'data\part_london\tq38sw_2m\rainfall.tif'

    building_data = np.loadtxt(building_path, skiprows=6)
    dem_data = np.loadtxt(dtm_path, skiprows=6)

    dem_add=np.add(building_data, dem_data)


    # get projection and geotransform information
    coordinate_info = gdal.Open(building_path)
    proj = coordinate_info.GetProjection()
    gtf = coordinate_info.GetGeoTransform()

    generateRainFall(coordinate_info, rainfall_path)

    # # Get GDAL driver GeoTiff
    # driver = gdal.GetDriverByName('GTiff')
    
    # # Get dimensions
    # nlines = dem_add.shape[0]
    # ncols = dem_add.shape[1]
    # nbands = len(dem_add.shape)
    # data_type = gdal.GDT_Int16 # gdal.GDT_Float32
    
    # # Create a temp grid
    # #options = ['COMPRESS=JPEG', 'JPEG_QUALITY=80', 'TILED=YES']
    # grid_data = driver.Create('grid_data', ncols, nlines, 1, data_type)#, options)
    
    # # Write data for each bands
    # grid_data.GetRasterBand(1).WriteArray(dem_add)
    
    # # Setup projection and geo-transform
    # grid_data.SetProjection(proj)
    # grid_data.SetGeoTransform(gtf)
    
    # # Save the file
    # driver.CreateCopy(dem_path, grid_data, 0)  
    
    # # Close the file
    # driver = None
    # grid_data = None
    
    # # Delete the temp grid
    # import os                
    # os.remove('grid_data')
    # #==================================================================

    # # save(h_sum, output_path)

    print("successful")



    
