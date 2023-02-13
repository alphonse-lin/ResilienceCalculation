from pypims import IO
import os
from pypims.IO.demo_functions import get_sample_data
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

dem_file, demo_data, data_path = get_sample_data() # get the path of sample data
# print(data_path)

# 1. DEM show
DEM = IO.Raster(os.path.join(data_path,'DEM.gz')) # load the file into a Raster object
# DEM.mapshow() # plot the Raster object

# rain_mask
rain_mask = IO.Raster(os.path.join(data_path,'rain_mask.gz'))
# rain_mask.mapshow()

# landcover show
landcover = IO.Raster(os.path.join(data_path,'landcover.gz'))
# test=landcover.mapshow()

# rain source show
rain_source = pd.read_csv(os.path.join(data_path,'rain_source.csv'), header = None)
# rain_source.head()

# gpu count
ngpus = 1



case_folder = os.path.join(os.getcwd(), 'hipims_case') # define a case folder in the current directory
print(case_folder)
case_input = IO.InputHipims(DEM, num_of_sections=ngpus, case_folder=case_folder)

case_input.set_initial_condition('h0',0.0)

# set stream
box_upstream = np.array([[1427, 195],  # bottom left
                         [1446, 243]]) # upper right
box_downstream = np.array([[58, 1645], # upper left
                           [72, 1170]]) # bottom right
discharge_values = np.array([[0, 100], # first column: time - s; second colum: discharge - m3/s
                            [3600,100]])

bound_list = [
            {'polyPoints': box_upstream,
             'type': 'open',
             'hU': discharge_values},
            {'polyPoints': box_downstream,
             'type': 'open',
             'h': np.array([[0, 5],
                            [3600,5]])}] # we fix the downstream depth as 12.5 m

case_input.set_boundary_condition(boundary_list=bound_list)
case_input.domain_show() # show domain map
# Flow series on boundary 1 is converted to velocities
# Theta = 135.00

rain_source_np = rain_source.to_numpy()
case_input.set_rainfall(rain_mask=rain_mask, rain_source=rain_source_np)

case_input.set_landcover(landcover)
case_input.set_grid_parameter(manning={'param_value': [0.035, 0.055],
                                        'land_value': [0, 1],
                                        'default_value':0.035})

case_input.set_gauges_position(np.array([[560, 1030],
                                        [1140,330]]))

case_input.set_runtime([0, 7200, 900, 1800])

print(case_input)
case_input.write_input_files()


# plt.show()