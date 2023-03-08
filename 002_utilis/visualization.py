from pypims import flood
import os
from pypims import IO
import re

dir_path=r'001_floodsim/hipims_case/output'

# def zill(path):
#     file=os.path.splitext(path)

#     os.rename(path, )


series=[]
files=os.listdir(dir_path)
files.sort()

for file in files:
    if not os.path.isdir(file):
        if "h_" in file and file.endswith('asc'):
            r_path=os.path.join(dir_path, file)
            ra=IO.Raster(r_path)
            series.append(ra)

path=r'001_floodsim/hipims_case/output/debug.gif'
IO.grid_show.make_gif(path,series)
# r_path=r'001_floodsim/hipims_case/output/h_0.asc'
# ra_1=IO.Raster(r_path)

# r_path=r'001_floodsim/hipims_case/output/h_900.asc'
# ra_2=IO.Raster(r_path)

# path=r'001_floodsim/hipims_case/output/debug.mp4'
# IO.grid_show.make_mp4(path,[ra_1, ra_2])