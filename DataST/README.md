# Javid_S2P_codes
Here you will find codes related to datastructure transformation of suite2p to Yaksi lab structure 

## dependencies 
- numpy 
- scipy

## Supports
- single channel
- dualchannel 
- single plane
- multiplane, plane bigger then two, no support for two planes, as it is assumed no data is created with two planes
- save as mat file, this is for matlab
- save as npy file, this is for numpy


## Data containtment
So far the transformed results contains the following data
1. volume
2. trace
3. position
4. neuronLabel

more data will be added soon.

## How to use 

### 1. Clone the repo
clone the repository local in your computer

>- <code> git clone https://github.com/yaksilab/Javid_S2P_codes/tree/main/DataST </code>

>- import the the module DataStructureTransform

>- <code> import DataStructureTransform* </code>

create a transform object using <code>Transform_results</code> object, do this by giving the object initilizer the nessecery parameters
1. first parameter is directory path, where your suite2p data is located
2. second parameter is factor_meter, this how big a pixel_size is
3. third parameter is total_z_distance, 
eksemple
<code> results_obj = Transform_results(directory, 0.3, 80) </code>

To retieve the transformed results

<code> results = results_obj.get_results() </code>

To save as npy file

<code> results_obj.save_as_npy() </code> This saves your transformed results to the same directory you have given for creatting the obj

To save as mat file 

<code> results_obj.save_as_npy() </code> This saves your transformed results to the same directory you have given for creatting the obj

### 2. Copy the code
Just copy the code and save it the same path as your working path with name DataStructureTransform
fowllow then the same procedure as Clone Repo


  
