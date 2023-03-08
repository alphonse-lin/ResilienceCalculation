import os
from pypims import IO
from pypims.IO.demo_functions import get_sample_data
import matplotlib.pyplot as plt
import pandas as pd
from utilis.general import timeCount, mkdir

if __name__ == '__main__':
    dir_path=r'001_floodsim/data/part_london/TQ27ne'

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
    dem.mapshow()

    ### read landcover
    landcover = IO.Raster(file_paths["landcover"])
    landcover.mapshow()

    ### read rainsources
    rain_mask = IO.Raster(file_paths["rainfall"])
    rain_mask.mapshow()

    ### rain source show
    rain_source = pd.read_csv(file_paths["rain_source"], header = None)
    # rain_source.head()
    # plt.show()

    ### gpu count
    ngpus = 1

    ### set output
    case_folder = r'001_floodsim/output/hipims_case'
    mkdir(case_folder)
    case_input = IO.InputHipims(dem, num_of_sections=ngpus, case_folder=case_folder)
    case_input.set_initial_condition('h0',0.0)

    # set rainfall
    rain_source_np = rain_source.to_numpy()
    case_input.set_rainfall(rain_mask=rain_mask, rain_source=rain_source_np)

    # set landcover
    case_input.set_landcover(landcover)

    # set manning
    case_input.set_grid_parameter(manning={'param_value': [0.035, 0.055],
                                            'land_value': [0, 1],
                                            'default_value':0.035})
    
    # set runtime
    case_input.set_runtime([0, 7200, 900, 1800])

    print(case_input)
    case_input.write_input_files()


    

    