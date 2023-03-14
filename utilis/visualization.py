from pypims import flood
import os
from pypims import IO
import re
import matplotlib.pyplot as plt

def exportGifFromDir(dir_path, output_path):
    series=[]
    files=os.listdir(dir_path)
    files.sort()

    for file in files:
        if not os.path.isdir(file):
            if "h_" in file and file.endswith('asc'):
                r_path=os.path.join(dir_path, file)
                ra=IO.Raster(r_path)
                series.append(ra)

    output_path=r'001_floodsim/hipims_case/output/debug.gif'
    IO.grid_show.make_gif(output_path,series)

def mapshow(path):
    dem = IO.Raster(path) # load the file into a Raster object
    dem.mapshow()

if __name__ == '__main__':
    # dir_path=r'001_floodsim/output/hipims_case/output'
    # exportGifFromDir(dir_path)

    path=r'001_floodsim/output/hipims_case/output/h_0.asc'
    mapshow(path)
    plt.show()


# def zill(path):
#     file=os.path.splitext(path)

#     os.rename(path, )



# r_path=r'001_floodsim/hipims_case/output/h_0.asc'
# ra_1=IO.Raster(r_path)

# r_path=r'001_floodsim/hipims_case/output/h_900.asc'
# ra_2=IO.Raster(r_path)

# path=r'001_floodsim/hipims_case/output/debug.mp4'
# IO.grid_show.make_mp4(path,[ra_1, ra_2])