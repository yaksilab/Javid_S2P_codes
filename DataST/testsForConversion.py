# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 14:23:40 2022

@author: Javid
"""
import matplotlib.pyplot as plt
import numpy as np

#import plotly
#import plotly.graph_objects as go

from DataStructureTransform import Transform_results

from binary import BinaryRWFile

directory1 = "X:/anna/Data/L-AP4 ex vivo/2023_01_05/20230105_10_01_05_AO_HuCGCaMP6s_21dpf_WASH_LAP4_exvivo_f001/suite2p"
directory2 = 'C:/YaksiData/Small data/suite2p' 
results_obj = Transform_results(directory1,True)

#Test for result
"""
print("testing general results")
results = results_obj.get_results['volume']
"""

#Test position


print("Testing Postion")

pos = np.transpose(results_obj.get_results['position'])
x ,y , z = pos[0], pos[1], pos[2]
#fig = go.Figure(data=[go.Scatter3d(x=x, y=y, z=z, mode='markers')])
#ig.show()
#print(pos[1])
#will 
plt.scatter(x, y)
plt.show()


#test volume
"""
vol = results_obj.get_results['volume']
print(np.shape(vol))
"""



#Test get_factMeter_distZ
"""
print("testing get_factMeter_distZ")
get_factMeter_distZ(directory2)
"""


#Test NeuronLabels

neuronLabels = results_obj.get_results['neuronLabels']
results = results_obj.get_results

#Testing position 
pos = results_obj.get_results['position']
print("this is shape of position:",np.shape(pos))


#Test Trace

#getting 
trace = results_obj.get_results['trace']
print(" this is the length of trace:", np.shape(trace))



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
    