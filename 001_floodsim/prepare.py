import sys
import numpy as np

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

def generateRaster(inDs, output_path):
    gt=inDs.GetGeoTransform()
    proj=inDs.GetProjection()
    rows = inDs.RasterYSize
    cols = inDs.RasterXSize

    # create the output image
    driver = inDs.GetDriver()
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
    outDs.SetGeoTransform(inDs.GetGeoTransform())
    outDs.SetProjection(inDs.GetProjection())

    del outData


if __name__ == '__main__':
    np.set_printoptions(suppress=True)
    # np.set_printoptions(threshold = np.inf) 

    path=r'data\part_london\extractedLondonDEM_2.tif'
    dem_output=r'data/part_london/dem.txt'
    rainfall_output=r'data/part_london/rainfall.txt'
    
    # ds=gdal.Open(path)

    # generateDEM(ds, dem_output)
    # generateRaster(ds, rainfall_output)

    
