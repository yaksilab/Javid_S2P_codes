# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 14:23:40 2022

@author: Javid
"""
import matplotlib.pyplot as plt
import numpy as np

import plotly.graph_objects as go

from DataStructureTransform import Transform_results
from UtilsForTransformation import create_px_position_list

directory1 = "C:/YaksiData/AnnData/Sixplanetiff/suite2p"
directory2 = 'C:/YaksiData/Small data/suite2p' 

#Test for result
"""
print("testing general results")
results_obj = Transform_results(directory1)
results = results_obj.get_results['volume']
"""

#Test position

print("Testing Postion")
results_obj = Transform_results(directory1)

pos = np.transpose(results_obj.get_results['position'])
x ,y , z = pos[0], pos[1], pos[2]
fig = go.Figure(data=[go.Scatter3d(x=x, y=y, z=z, mode='markers')])
fig.show()


#Test get_factMeter_distZ
"""
print("testing get_factMeter_distZ")
get_factMeter_distZ(directory2)
"""

