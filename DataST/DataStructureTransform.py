# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 12:31:53 2022

@author: Javid
"""

import numpy as np
import scipy.io

def save_results_mat_fil(results: dict, directory: str):
    scipy.io.savemat(directory+'/results.mat',results)
    print(f'your results is saved in the directory: {directory} as a results.npy file')
    return 1

def save_results(results: dict ,directory:str):
    np.save(directory+'/results',results)
    print(f'your results is saved in the directory: {directory} as a results.npy file')
    return 1

def transform_results(directory:str)->dict:
    results = {}
    ops = np.load(directory+'/plane0/ops.npy',allow_pickle=True)
    ops = ops.item()
    nplanes = ops['nplanes']
    
    Lx, Ly = ops['Lx'], ops['Ly']
    
    if nplanes == 1:
        results['volume'] = ops['meanImg']
        results['trace'] = np.load(directory+'/plane0/F.npy',allow_pickle=True)
        
        
    else:
        ops_combined = np.load(directory+'/combined/ops.npy',allow_pickle= True)
        ops_combined = ops_combined.item()
        
        volume = np.empty(shape=(nplanes, Ly, Lx))
        Lx_combined, Ly_combined = ops_combined['Lx'], ops_combined['Ly']
    
        
        mean_image = ops_combined['meanImg']
        plane = 0
        
        for i in range(int(Lx_combined/Lx)):
            
            for j in range(int(Ly_combined/Ly)):
                
                A = mean_image[j*Ly : (j+1)*Ly , i*Lx : (i+1)*Lx]
                volume[plane,:,:] = A
                plane+=1
                
        results['volume'] = volume
        results['trace'] = np.load(directory+'/combined/F.npy',allow_pickle = True)
        results = {'results':results}
    return results
        
            