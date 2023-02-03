# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 16:01:16 2022

@author: Javid
"""
import numpy as np
import os 
import re






def get_metadata(directory):

    meta_data = {"experiment.name": "","experiment.type": "",r"volume.rate.\(in.Hz\)": "","x.pixel.sz": "","total.z.distance": ""}
    file_list = os.listdir(directory)
    for file in file_list:
        if file.endswith(".ini"):

            with open(os.path.join(directory, file)) as f:
                value = f.read()
                
                for key in meta_data.keys():                 
                    try: 
                        i = re.search(key, value).end()
                    except AttributeError:
                        print(f"no value found for {key}")
                        continue
                    for char in value[i+3:]:
                        if char =='\n':
                            break
                        meta_data[key] +=char
                    
    return meta_data
            
                
                
directory = 'C:/YaksiData/AnnData/Sixplanetiff/suite2p' 
#print(get_metadata(directory))

       

