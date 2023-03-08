{
    "grid_attr": {
        "area": "[4351200.0, 'm^2']",
        "shape": "(269, 269)",
        "cellsize": "[10.0, 'm']",
        "num_cells": 43512,
        "extent": {
            "left": 0.0,
            "right": 2690.0,
            "bottom": 0.0,
            "top": 2690.0
        }
    },
    "model_attr": {
        "case_folder": "001_floodsim/sample_code/hipims_case",
        "birthday": "2023-03-08 20:06",
        "num_GPU": 1,
        "run_time": "[0, 7200, 900, 1800]",
        "num_gauges": 2
    },
    "initial_attr": {
        "h0": 0.0,
        "hU0x": 0,
        "hU0y": 0
    },
    "boundary_attr": {
        "num_boundary": 3,
        "boundary_details": "['0. (outline) fall, h and hU fixed as zero, number of cells: 788', '1. open, hU given, number of cells: 2', '2. open, h given, number of cells: 46']"
    },
    "rain_attr": {
        "num_source": 4,
        "max": "[50.0, 'mm/h']",
        "sum": "[12.38, 'mm']",
        "average": "[13.75, 'mm/h']",
        "spatial_res": "[924.0, 'm']",
        "temporal_res": "[360.0, 's']"
    },
    "params_attr": {
        "manning": {
            "param_value": [
                0.035,
                0.055
            ],
            "land_value": [
                0,
                1
            ],
            "default_value": 0.035
        },
        "sewer_sink": 0,
        "cumulative_depth": 0,
        "hydraulic_conductivity": 0,
        "capillary_head": 0,
        "water_content_diff": 0
    }
}