# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 16:01:16 2022

@author: Javid
"""
import numpy as np
import os 
import re




def add_volume(directory : str, volume,plane_nr):
    

    ops = np.load(directory+'/plane'+str(plane_nr)+ '/ops.npy',allow_pickle=True).item()
            
    meanImg = ops['meanImg']
    
    volume[plane_nr] = meanImg
    
    
def add_trace(directory : str, trace, plane_nr):
    
    F_roi = np.load(directory+'/plane'+str(plane_nr)+'/F.npy', allow_pickle=True)
    
    
    iscell = np.load(directory+'/plane'+str(plane_nr)+ '/iscell.npy',allow_pickle=True)
    
    bool_iscell = np.array([True if roi[0]==1 else False for roi in iscell])
    
    F_cell = F_roi[bool_iscell]
    print(np.shape(F_cell))
    
    frame_diff = np.shape(trace)[1]-np.shape(F_cell)[1]
    
    if frame_diff <0:
        c = np.zeros((np.shape(trace)[0],abs(frame_diff)))#maybe need to add data type float32
        trace = np.append(trace,c, axis = 1)
    elif frame_diff >0:
        
        c = np.zeros((np.shape(F_cell)[0],abs(frame_diff)))# maybe need to add data type float32
        F_cell = np.append(F_cell,c,axis = 1)
        print(np.shape(F_cell))
        
    return np.append(trace,F_cell,axis =0)
    
def create_px_position_list(directory: str, nr_of_planes):
    
    px_position_list = []
    

    
    if nr_of_planes == 1:
        
        roi_stat = np.load(directory+'/Plane0/stat.npy',allow_pickle = True)
        iscell = np.load(directory+'/Plane0/iscell.npy',allow_pickle = True)
        bool_iscell = np.array([True if roi[0]==1 else False for roi in iscell])
        cell_stat = roi_stat[bool_iscell]
        totall_nr_of_cells = len(cell_stat)
        
        pixel_position = np.empty(shape = (totall_nr_of_cells,5))
        
        for cell_nr, cell in enumerate(cell_stat):
            y_px, x_px = cell['med']
            
            
            
            pixel_position[cell_nr] = [x_px, y_px, nr_of_planes, cell_nr, nr_of_planes]
            px_position_list.append(pixel_position)
        
        return px_position_list
    
    else:
        
        cell_count = 0
        
        for plane_nr in range(nr_of_planes):
            
            roi_stat = np.load(directory+'/Plane'+str(plane_nr)+'/stat.npy',allow_pickle = True)
            iscell = np.load(directory+'/Plane'+str(plane_nr)+'/iscell.npy',allow_pickle = True)
            bool_iscell = np.array([True if roi[0]==1 else False for roi in iscell])
            
            cell_stat = roi_stat[bool_iscell]
            
            nr_of_cells = len(cell_stat)
            
            cell_count += nr_of_cells
            
            px_position = np.empty(shape = (nr_of_cells,5))
            
            for cell_nr, cell in enumerate(cell_stat):
                
                y_px, x_px = cell['med']
                
                
                if plane_nr ==0:
                    
                    px_position[cell_nr] = [x_px, y_px, nr_of_planes -2 , cell_nr + cell_count, nr_of_planes -2]
                    
                elif plane_nr ==1:
                    px_position[cell_nr] = [x_px, y_px, nr_of_planes -1 , cell_nr + cell_count, nr_of_planes -1]
                    
                else:
                    px_position[cell_nr] = [x_px, y_px, plane_nr-1 , cell_nr + cell_count, plane_nr -1]
                    
            px_position_list.append(px_position)
            
    return np.roll(px_position_list,-2, axis = 0)
                                     
                    
def calculate_space_postion(pixel_position_list,factor_meter,Ly):
    
    
    nb_planes =  len(pixel_position_list)
    
    
    if nb_planes == 1:
        m = np.transpose(pixel_position_list[0])
        
        m[0],m[1] = m[0]*factor_meter,m[1]*factor_meter
        return [np.transpose(m)]
        
    else:
        dist_z = 80 #in micrometers
        step_z = dist_z/(nb_planes-1)
        maxY  = Ly*factor_meter
        alpha = np.arcsin(step_z/maxY)
        
        
        horiz_plane = np.sqrt(maxY**2+step_z**2)
        returnning_plane = np.sqrt(horiz_plane**2+(7*step_z)**2)
        fact = returnning_plane/maxY
        factor_meter_returning_plane = factor_meter*fact
        
        maxY_returning_plane = Ly*factor_meter_returning_plane
        beta = np.arcsin(7*step_z/maxY_returning_plane)
        
        
        initial_depth = [0, step_z, 2*step_z, 3*step_z, 4*step_z, 5*step_z, 6*step_z, 7*step_z]
        final_depth   = [step_z, 2*step_z, 3*step_z, 4*step_z, 5*step_z, 6*step_z, 7*step_z, 0]
        
        for plane_nr, plane in enumerate(pixel_position_list):
            
            
            if plane_nr+1 == nb_planes:
                m = np.transpose(plane)
                
                x = m[0]*factor_meter
                y = m[1]*factor_meter_returning_plane
                z_new = (y/maxY_returning_plane*(final_depth[plane_nr] \
                                                    -initial_depth[plane_nr])) + initial_depth[plane_nr]
               
                    
                #z_new2 = y*np.sin(beta) + initial_depth[plane_nr] # dont know why this is included
                y_new = y*np.cos(beta)
                
                np.transpose(pixel_position_list[plane_nr])[0] = x
                np.transpose(pixel_position_list[plane_nr])[1] = y_new
                np.transpose(pixel_position_list[plane_nr])[2] = z_new
                
            else:
                m = np.transpose(plane)
                
                x = m[0]*factor_meter
                y = m[1]*factor_meter
                z_new = (y/maxY*(final_depth[plane_nr] \
                                                    - initial_depth[plane_nr])) + initial_depth[plane_nr]
               
                    
                #z_new2 = y*np.sin(alpha) + initial_depth[plane_nr] # dont know why this is included
                y_new = y*np.cos(alpha)
                
                np.transpose(pixel_position_list[plane_nr])[0] = x
                np.transpose(pixel_position_list[plane_nr])[1] = y_new
                np.transpose(pixel_position_list[plane_nr])[2] = z_new
                
        return np.vstack(pixel_position_list)                 
            
            

def add_neuronLabels(directory,results,nr_of_planes,Lx, Ly):
   
    print('Lx: ',Lx,'Ly: ',Ly)
    
    neuronLabels = np.zeros(shape = (nr_of_planes,Ly,Lx))
    
    
    for plane in range(nr_of_planes):
    
        roi_stat = np.load(directory+'/Plane'+str(plane)+ '/stat.npy',allow_pickle = True)
        iscell = np.load(directory+'/Plane'+str(plane)+'/iscell.npy',allow_pickle = True)
        bool_iscell = np.array([True if roi[0]==1 else False for roi in iscell])
        
        cell_stat = roi_stat[bool_iscell]
        
        cell_count  = 0
        
        for cell_nr, cell in enumerate(cell_stat):
            cell_count+=1
            
            X,Y = cell['xpix'][~cell['overlap']],cell['ypix'][~cell['overlap']]
            
            for x,y in zip(X,Y):
                neuronLabels[plane,y,x] = cell_nr+cell_count
                

    results['neuronLabels'] = np.roll(neuronLabels,-2,axis=0)
    


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

       

