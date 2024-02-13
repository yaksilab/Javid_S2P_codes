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
        
        
        new_nr_of_planes = nr_of_planes
        if not last_plane and nr_of_planes>1:  #weather to include the last plane in the results file.
            new_nr_of_planes = nr_of_planes-1 #if include then runs thor all processed planes
            
        
        metadata['dim'] = [Lx,Ly,new_nr_of_planes,nr_of_frames]                  
      
        pixel_position_list = self.__create_px_position_list(directory, nr_of_planes)[:new_nr_of_planes]
        nr_of_cells = np.sum([len(s) for s in pixel_position_list])
        
        volume = np.empty(shape = (nr_of_planes,Ly,Lx))
        trace = []
        trace2 = []
        spks = []

        
        
        for plane_nr in range(nr_of_planes):

            self.__add_volume(directory, volume, plane_nr)
            self.__add_trace(directory, trace, trace2, plane_nr,nr_of_frames)
            self.__add_spks(directory, spks, plane_nr, nr_of_frames)
            
        trace = np.array(trace,dtype=object)
        trace2 = np.array(trace2,dtype=object)
        spks = np.array(spks,dtype=object)
        

        results['volume'] = np.transpose(np.roll(volume,-2, axis = 0)[:new_nr_of_planes]) #original shape is (nr_planes,lx,ly), after transpose shape = (ly,lx,nr_planes)
        print('Added volume')
        print()
        results['trace'] = np.vstack(np.roll(trace, -2, axis= 0)[:new_nr_of_planes])
        if int(float(metadata["no.of.channels"])) == 2:
            results['trace_ch_2'] = np.vstack(np.roll(trace2, -2, axis= 0)[:new_nr_of_planes])
        print('Added Trace with number of cells:', len(np.vstack(np.roll(trace, -2, axis= 0)[:new_nr_of_planes])))
        print()
        results['position'] = self.__calculate_space_postion(pixel_position_list[:new_nr_of_planes], metadata, Ly,nr_of_planes,nr_of_cells)
        print('Added position')
        print()
        self.__add_neuronLabels(directory, results, nr_of_planes, Lx, Ly,new_nr_of_planes)
        print('Added neuronLabels')
        print()
        results['metadata'] = metadata
        print('Added metadata')
        results['spks']= spks
        print("added the deconvolved traces")
        
        return results
        

    def __add_volume(self,directory : str, volume,plane_nr):
        

        ops = np.load(directory+'/plane'+str(plane_nr)+ '/ops.npy',allow_pickle=True).item()
                
        meanImg = ops['meanImg']
        
        volume[plane_nr] = meanImg
        
        
        
    def __add_trace(self,directory : str, trace, trace2, plane_nr,nr_of_frames):
        
        ch2: bool = False
        
        F_roi = np.load(directory+'/plane'+str(plane_nr)+'/F.npy', allow_pickle=True)
        iscell = np.load(directory+'/plane'+str(plane_nr)+ '/iscell.npy',allow_pickle=True)
        bool_iscell = np.array([True if roi[0]==1 else False for roi in iscell])
        F_cell = F_roi[bool_iscell]
        

        try:
            F_roi2 = np.load(directory+'/plane'+str(plane_nr)+'/F_chan2.npy', allow_pickle=True)
            F_cell2 = F_roi2[bool_iscell]
            ch2 = not ch2
        except FileNotFoundError:
            print("no channel 2 present")
            
            
        
        frame_diff = nr_of_frames -np.shape(F_cell)[1] #this is if there are frames that are excluded
        
        
        if frame_diff <0:
            c = np.zeros((np.shape(trace)[0],abs(frame_diff)))#maybe need to add data type float32
            trace = np.append(trace,c, axis = 1)
            if ch2:
              trace2 = np.append(trace2,c, axis = 1)
            
        elif frame_diff >0:
            
            c = np.zeros((np.shape(F_cell)[0],abs(frame_diff)))# maybe need to add data type float32
            F_cell = np.append(F_cell,c,axis = 1)
            if ch2:
              F_cell2 = np.append(F_cell2,c,axis= 1)
            
        trace.append(F_cell)
        if ch2:
          trace2.append(F_cell2)
        
        
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
            
           
            return np.array(px_position_list,dtype=object)
        
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
                
        px_position_list = np.roll(np.array(px_position_list,dtype=object),-2, axis = 0)
      
        return px_position_list
                                         
                        
    def __calculate_space_postion(self,pixel_position_list,metadata,Ly,nr_of_planes,nr_of_cells):
        
        
        factor_meter = float(metadata['x.pixel.sz'])*10**7
        nb_planes =  nr_of_planes

        if nb_planes == 1:
            
            m = np.transpose(pixel_position_list[0])
            
            m[0],m[1] = m[0]*factor_meter,m[1]*factor_meter
            return np.transpose(m)
            
        else:
            dist_z = float(metadata['total.z.distance'])
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
        
        neuronLabels = np.zeros(shape = (Lx,Ly,new_nr_of_planes,))
        plane_cell_stat_list = []
        
        for plane in range(nr_of_planes):
        
            roi_stat = np.load(directory+'/Plane'+str(plane)+ '/stat.npy',allow_pickle = True)
            iscell = np.load(directory+'/Plane'+str(plane)+'/iscell.npy',allow_pickle = True)
            bool_iscell = np.array([True if roi[0]==1 else False for roi in iscell])
            
            cell_stat = roi_stat[bool_iscell]
            plane_cell_stat_list.append(cell_stat)
            
        plane_cell_stat_list = np.roll(np.array(plane_cell_stat_list,dtype=object), -2,axis = 0)
        
        cell_count  = 0
        for plane_nr, cell_stat in enumerate(plane_cell_stat_list[:new_nr_of_planes]):
            
            for cell_nr, cell in enumerate(cell_stat,start=cell_count+1):
                cell_count +=1
                X,Y = cell['xpix'][~cell['overlap']],cell['ypix'][~cell['overlap']]
              
                for x,y in zip(X,Y):
                    
                    neuronLabels[x,y,plane_nr] = cell_nr
        print("cekk_ciunt in neuronlabels:", cell_count)

        results['neuronLabels'] = neuronLabels
        

    def __add_spks(self,directory: str, spks, plane_nr, nr_of_frames):
        spks_roi = np.load(directory+'/plane'+str(plane_nr)+'/spks.npy', allow_pickle=True)
        iscell = np.load(directory+'/plane'+str(plane_nr)+ '/iscell.npy',allow_pickle=True)
        bool_iscell = np.array([True if roi[0]==1 else False for roi in iscell])
        spks_cell = spks_roi[bool_iscell]

        frame_diff = nr_of_frames -np.shape(spks_cell)[1] #this is if there are frames that are excluded
        
        
        if frame_diff <0:
            c = np.zeros((np.shape(spks)[0],abs(frame_diff)))#maybe need to add data type float32
            spks = np.append(spks,c, axis = 1)
        elif frame_diff >0:
            
            c = np.zeros((np.shape(spks_cell)[0],abs(frame_diff)))# maybe need to add data type float32
            F_cell = np.append(spks_cell,c,axis = 1)
            
        spks.append(spks_cell)
        