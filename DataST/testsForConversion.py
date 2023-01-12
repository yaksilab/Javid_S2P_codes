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
from binary import BinaryRWFile

directory1 = "C:/YaksiData/AnnData/Sixplanetiff/suite2p"
directory2 = 'C:/YaksiData/Small data/suite2p' 
results_obj = Transform_results(directory1)

#Test for result
"""
print("testing general results")
results = results_obj.get_results['volume']
"""

#Test position
"""
print("Testing Postion")


pos = np.transpose(results_obj.get_results['position'])
x ,y , z = pos[0], pos[1], pos[2]
fig = go.Figure(data=[go.Scatter3d(x=x, y=y, z=z, mode='markers')])
fig.show()
print(pos[1])

plt.scatter(x, y)
plt.show()
"""
#Test get_factMeter_distZ
"""
print("testing get_factMeter_distZ")
get_factMeter_distZ(directory2)
"""
#Test NeuronLabels
#neuronLabels = results_obj.get_results['neuronLabels']
results = results_obj.get_results

print(np.shape(results['neuronLabels']))
print()



#Test Trace
"""
trace = results_obj.get_results['trace']
print(len(trace))


print(trace[0])
print(trace[1])
print(trace[2])
"""
"""
results_obj.save_as_mat()
results = results_obj.get_results
print(results['metadata'])"""


#how to open binary file in numpy format
"""
reg_bin = "C://YaksiData//Small data//suite2p//plane0//data.bin"
Lx = 512
Ly = 510


with BinaryRWFile(Ly=Ly, Lx=Lx, filename=reg_bin) as f_raw:
    print(f_raw[0])
"""    
    