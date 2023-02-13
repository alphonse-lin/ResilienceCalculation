import os
from pypims import IO
from pypims.IO.demo_functions import get_sample_data

dem_file, demo_data, data_path = get_sample_data() # get the path of sample data
# print(data_path)

# DEM show
DEM = IO.Raster(os.path.join(data_path,'DEM.gz')) # load the file into a Raster object

ngpus = 1
case_folder = os.path.join(os.getcwd(), 'hipims_case') # define a case folder in the current directory
case_input = IO.InputHipims(DEM, num_of_sections=ngpus, case_folder=case_folder)

case_output = IO.OutputHipims(input_obj = case_input)
print(case_output)

gauges_pos, times, values = case_output.read_gauges_file(file_tag = 'h')


import matplotlib.pyplot as plt
lines = plt.plot(times, values)
plt.xlabel('time (s)')
plt.ylabel('depth (m)')
plt.legend(lines[:2],['downstream','upstream'])

max_depth = case_output.read_grid_file(file_tag='h_max_7200')
max_depth.mapshow()

plt.show()