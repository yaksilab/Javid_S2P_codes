

# Javid_S2P_codes
Here you will find codes related to datastructure transformation of suite2p to Yaksi lab structure 

Table of contents
=================
<!--ts-->
   * [Dependencies](#Dependencies)
   * [Supports](#Supports)
   * [Data containtment](#Data-containtment)
   * [Dependency](#dependency)
   * [How to use](#How-to-use)
     * [1. Clone](#clone)
     * [2. Copy the code](#copy)
<!--te-->


## Dependencies 
- numpy 
- scipy

## Supports
- single channel
- dualchannel 
- single plane
- multiplane (**no support for two and three planes**)
- save as mat file, this is for matlab
- save as npy file, this is for numpy


## Data containtment
So far the transformed results contains the following data
1. volume
2. trace
3. position
4. neuronLabel
5. metadata

More data from suite2p can be added, open an issue for such.

## How to use 

### 1. Clone the repo <a id='clone'></a>
clone the repository local in your computer

>- <code> git clone https://github.com/yaksilab/Javid_S2P_codes/tree/main/DataST </code>

import the the module DataStructureTransform

>- <code> import DataStructureTransform* </code>

First it is **Important that you have a copy of your config file in the suite2p folder** that you want to convert the data from.

create a transform object using <code>Transform_results</code> object, do this by giving the object initilizer the nessecery parameters
1. first parameter is directory path, where your suite2p data is located
2. second parameter (optional), weather if you want to include the last plane in your recording. Default value is False. 

 
Eksemple:

>- <code> results_obj = Transform_results(directory) </code>

To retieve the transformed results

>- <code> results = results_obj.get_results </code>

To save as npy file

>- <code> results_obj.save_as_npy() </code> This saves your transformed results to the same directory you have given for creatting the obj

To save as mat file 

>- <code> results_obj.save_as_npy() </code> This saves your transformed results to the same directory you have given for creatting the obj

### 2. Copy the code<a id='copy'></a>
Just copy the code and save it the same path as your working path with name DataStructureTransform
fowllow then the same procedure as Clone Repo


  
