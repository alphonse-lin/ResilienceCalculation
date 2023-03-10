from osgeo import gdal, osr
import os

if __name__ == '__main__':
    dem_path=r'data\part_london\part\TQ27ne_DTM_1m.tif'
    
    input_file =r'data\output\asc\velocity\hU_7200.asc'
    output_file = r'data\output\asc\velocity\hU_7200.tif'

    # open input file
    input_dataset = gdal.Open(input_file)
    dem_dataset = gdal.Open(dem_path)

    # get input file parameters
    cols = input_dataset.RasterXSize
    rows = input_dataset.RasterYSize
    # get projection and geotransform information
    projection = dem_dataset.GetProjection()
    geotransform = dem_dataset.GetGeoTransform()

    # create output file
    driver = gdal.GetDriverByName('GTiff')
    output_dataset = driver.Create(output_file, cols, rows, 1, gdal.GDT_Float32)

    # set output file parameters
    output_dataset.SetGeoTransform(geotransform)
    output_dataset.SetProjection(projection)

    # write data to output file
    output_dataset.GetRasterBand(1).WriteArray(input_dataset.GetRasterBand(1).ReadAsArray())

    # close input and output datasets
    input_dataset = None
    output_dataset = None
    print("successful")