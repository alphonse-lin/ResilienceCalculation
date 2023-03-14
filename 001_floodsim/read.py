import os
from pypims import IO
from pypims.IO.demo_functions import get_sample_data
import matplotlib.pyplot as plt
import pandas as pd
import time

import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
# __file__获取执行文件相对路径，整行为取上一级的上一级目录
sys.path.append(BASE_DIR)
from utilis.general import timeCount, mkdir


if __name__ == '__main__':
    t_start = time.time()
    dir_path=r'001_floodsim/data/part_london/tq38sw'

    file_paths={"dem":"", "landcover":"", "rainfall":"", "rain_source":""}
    files=os.listdir(dir_path)
    for file in files:
        if "dem" in file:
            file_paths["dem"]=os.path.join(dir_path, file)
            continue
        elif "landcover" in file:
            file_paths["landcover"]=os.path.join(dir_path, file)
            continue
        elif "rainfall" in file:
            file_paths["rainfall"]=os.path.join(dir_path, file)
            continue
        elif "rain_source" in file:
            file_paths["rain_source"]=os.path.join(dir_path, file)
            continue
        else:
            continue
    
    
    ### read dem
    dem = IO.Raster(file_paths["dem"]) # load the file into a Raster object
    # dem.mapshow()
    timeCount('load dem', t_start)

    ### read landcover
    landcover = IO.Raster(file_paths["landcover"])
    # landcover.mapshow()
    timeCount('load landcover', t_start)


    ### read rainsources
    rain_mask = IO.Raster(file_paths["rainfall"])
    # rain_mask.mapshow()
    timeCount('load rainmask', t_start)


    ### rain source show
    rain_source = pd.read_csv(file_paths["rain_source"], header = None)
    # rain_source.head()
    # plt.show()
    timeCount('load rainsource', t_start)


    ### gpu count
    ngpus = 1

    ### set output
    case_folder = r'001_floodsim/output/hipims_case'
    mkdir(case_folder)
    case_input = IO.InputHipims(dem, num_of_sections=ngpus, case_folder=case_folder)
    case_input.set_initial_condition('h0',0.0)
    timeCount('set_initial_condition', t_start)

    # set rainfall
    rain_source_np = rain_source.to_numpy()
    case_input.set_rainfall(rain_mask=rain_mask, rain_source=rain_source_np)
    timeCount('set_rainfall', t_start)

    # set landcover
    case_input.set_landcover(landcover)
    timeCount('set_landcover', t_start)


    # set manning
    case_input.set_grid_parameter(manning={'param_value': [0.035, 0.055],
                                            'land_value': [0, 1],
                                            'default_value':0.035})
    timeCount('set_manning', t_start)
    
    # set runtime
    case_input.set_runtime([0, 7200, 450, 1800])
    timeCount('set_runtime', t_start)

    print(case_input)
    case_input.write_input_files()


    

    