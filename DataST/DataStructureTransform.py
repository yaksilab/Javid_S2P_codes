# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 12:31:53 2022

@author: Javid
"""
import numpy as np
import scipy.io
from UtilsForTransformation import *



class Transform_results:
    
    
    
    def __init__(self,directory:str,last_plane = False):
        self.__results = self.__transform_results(directory,last_plane)
        self.directory = directory
        
        
    @property
    def get_results(self):
        return self.__results
    
      
    def save_as_npy(self):
        np.save(self.directory+'/results',self.__results)
        print(f'your results is saved in the directory: {self.directory} as a results.npy file')
    
    
    def save_as_mat(self):
        scipy.io.savemat(self.directory+'/results.mat',self.__results)
        print(f'your results is saved in the directory: {self.directory} as a results.mat file')
    
    def __transform_results(self,directory: str,last_plane) ->dict:
        results = {}
        
        ops = np.load(directory+'/plane0/ops.npy',allow_pickle=True).item() 
        
        nr_of_planes = ops['nplanes']
        Lx, Ly = ops['Lx'], ops['Ly']
        nr_of_frames = ops['nframes']
        metadata = get_metadata(directory)
        
        
        factor_meter, dist_z = float(metadata['x.pixel.sz'])*10**7,float(metadata['total.z.distance'])
        
        
        
        new_nr_of_planes = nr_of_planes
        if not last_plane and nr_of_planes>1:  #weather to include the last plane in the results file.
            new_nr_of_planes = nr_of_planes-1 #if include then runs thor all processed planes
            #nr_of_cells = nr_of_cells - len(pixel_position_list[-1])
        
        metadata['dim'] = [Lx,Ly,new_nr_of_planes,nr_of_frames]                  
        
        pixel_position_list , nr_of_cells = self.__create_px_position_list(directory, new_nr_of_planes)
        
        volume = np.empty(shape = (nr_of_planes,Ly,Lx))
        trace = []
        
        
        for plane_nr in range(nr_of_planes):

            self.__add_volume(directory, volume, plane_nr)
            self.__add_trace(directory, trace, plane_nr,nr_of_frames)

        results['volume'] = np.transpose(np.roll(volume,-2, axis = 0)[:new_nr_of_planes]) #original shape is (nr_planes,lx,ly), after transpose shape = (ly,lx,nr_planes)
        print('Added volume')
        print()
        results['trace'] = np.vstack(np.roll(trace, -2, axis= 0)[:new_nr_of_planes])
        print('Added Trace')
        print()
        results['position'] = self.__calculate_space_postion(pixel_position_list[:new_nr_of_planes], factor_meter, Ly,dist_z,nr_of_planes,nr_of_cells)
        print('Added position')
        print()
        self.__add_neuronLabels(directory, results, nr_of_planes, Lx, Ly,new_nr_of_planes)
        print('Added neuronLabels')
        print()
        results['metadata'] = metadata
        print('Added metadata')
        
        return results
        

    def __add_volume(self,directory : str, volume,plane_nr):
        

        ops = np.load(directory+'/plane'+str(plane_nr)+ '/ops.npy',allow_pickle=True).item()
                
        meanImg = ops['meanImg']
        
        volume[plane_nr] = meanImg
        
        
        
    def __add_trace(self,directory : str, trace, plane_nr,nr_of_frames):
        
        F_roi = np.load(directory+'/plane'+str(plane_nr)+'/F.npy', allow_pickle=True)
        
        
        iscell = np.load(directory+'/plane'+str(plane_nr)+ '/iscell.npy',allow_pickle=True)
        
        bool_iscell = np.array([True if roi[0]==1 else False for roi in iscell])
        
        F_cell = F_roi[bool_iscell]
        #print(np.shape(F_cell))
        
        frame_diff = nr_of_frames -np.shape(F_cell)[1] #this is if there are frames that are excluded
        
        
        if frame_diff <0:
            c = np.zeros((np.shape(trace)[0],abs(frame_diff)))#maybe need to add data type float32
            trace = np.append(trace,c, axis = 1)
        elif frame_diff >0:
            
            c = np.zeros((np.shape(F_cell)[0],abs(frame_diff)))# maybe need to add data type float32
            F_cell = np.append(F_cell,c,axis = 1)
            #print(np.shape(F_cell))
        trace.append(F_cell)
        #return np.append(trace,F_cell,axis =0)
        
    def __create_px_position_list(self,directory: str, nr_of_planes):
        
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
            
            return px_position_list,totall_nr_of_cells
        
        else:
            
            cell_count = 0
            
            for plane_nr in range(nr_of_planes):
                
                roi_stat = np.load(directory+'/Plane'+str(plane_nr)+'/stat.npy',allow_pickle = True)
                iscell = np.load(directory+'/Plane'+str(plane_nr)+'/iscell.npy',allow_pickle = True)
                bool_iscell = np.array([True if roi[0]==1 else False for roi in iscell])
                
                cell_stat = roi_stat[bool_iscell]
                
                nr_of_cells = len(cell_stat)
                
                px_position = np.empty(shape = (nr_of_cells,5))
                
                for cell_nr, cell in enumerate(cell_stat):
                    
                    y_px, x_px = cell['med']
                    
                    
                    if plane_nr ==0:
                        
                        px_position[cell_nr] = [x_px, y_px, nr_of_planes -2 , cell_nr + cell_count, nr_of_planes -1]
                        
                    elif plane_nr ==1:
                        px_position[cell_nr] = [x_px, y_px, nr_of_planes -1 , cell_nr + cell_count, nr_of_planes]
                        
                    else:
                        px_position[cell_nr] = [x_px, y_px, plane_nr-1 , cell_nr + cell_count, plane_nr -1]
                cell_count += nr_of_cells        
                px_position_list.append(px_position)
                
        return np.roll(px_position_list,-2, axis = 0),cell_count
                                         
                        
    def __calculate_space_postion(self,pixel_position_list,factor_meter,Ly,dist_z,nr_of_planes,nr_of_cells):
        
        
        nb_planes =  nr_of_planes

        if nb_planes == 1:
            m = np.transpose(pixel_position_list[0])
            
            m[0],m[1] = m[0]*factor_meter,m[1]*factor_meter
            return [np.transpose(m)]
            
        else:
            #dist_z = 80 #in micrometers
            
            step_z = dist_z/(nb_planes-1)
            maxY  = Ly*factor_meter
            alpha = np.arcsin(step_z/maxY)
        
            
            
            horiz_plane = np.sqrt(maxY**2+step_z**2)
            returnning_plane = np.sqrt(horiz_plane**2+((nb_planes-1)*step_z)**2)
            fact = returnning_plane/maxY
            factor_meter_returning_plane = factor_meter*fact
            
            maxY_returning_plane = Ly*factor_meter_returning_plane
            beta = np.arcsin((nb_planes-1)*step_z/maxY_returning_plane)
            
            initial_depth = [i*step_z for i in range(nb_planes)]
            final_depth = [(i+1)*step_z for i in range(nb_planes-1)]
            final_depth.append(0)
            
            #initial_depth = [0, step_z, 2*step_z, 3*step_z, 4*step_z, 5*step_z, 6*step_z, 7*step_z]
            #final_depth   = [step_z, 2*step_z, 3*step_z, 4*step_z, 5*step_z, 6*step_z, 7*step_z, 0]
            
            cell_index = np.arange(1,nr_of_cells+1)
            
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
                    print("calculated returning plane postiton")
                    
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
                    
            position_matrix = np.vstack(pixel_position_list)  
            np.transpose(position_matrix)[3] = cell_index
            return position_matrix               
                                

    def __add_neuronLabels(self,directory,results,nr_of_planes,Lx, Ly,new_nr_of_planes):
       
        #print('Lx: ',Lx,'Ly: ',Ly)
        
        neuronLabels = np.zeros(shape = (Lx,Ly,new_nr_of_planes,))
        plane_cell_stat_list = []
        
        for plane in range(new_nr_of_planes):
        
            roi_stat = np.load(directory+'/Plane'+str(plane)+ '/stat.npy',allow_pickle = True)
            iscell = np.load(directory+'/Plane'+str(plane)+'/iscell.npy',allow_pickle = True)
            bool_iscell = np.array([True if roi[0]==1 else False for roi in iscell])
            
            cell_stat = roi_stat[bool_iscell]
            plane_cell_stat_list.append(cell_stat)
            
        plane_cell_stat_list = np.roll(plane_cell_stat_list, -2,axis = 0)
        
        cell_count  = 0
        for plane_nr, cell_stat in enumerate(plane_cell_stat_list[:new_nr_of_planes]):
            
            for cell_nr, cell in enumerate(cell_stat):
                cell_count+=1
                X,Y = cell['xpix'][~cell['overlap']],cell['ypix'][~cell['overlap']]
                
                for x,y in zip(X,Y):
                    neuronLabels[x,y,plane_nr] = cell_nr+cell_count ##Change the index here
            
        
        results['neuronLabels'] = neuronLabels
        

