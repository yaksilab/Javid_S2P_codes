

# Javid_S2P_codes
Here you will find codes related to datastructure transformation of suite2p to Yaksi lab structure 

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
3. spike
4. position
5. neuronLabel
6. metadata

More data from suite2p can be added, open an issue for such.

## How to use 

### 1. Creat a conda environment
There an environment file `environment.yml` in the root directory of this repository [environment.yaml](environment.yaml), you need to download it and create a conda environment using the following command:

```bash
conda env create -f environment.yaml
```

it is simple conda environment

```
name: DataST
channels:
  - conda-forge
  - defaults
dependencies:
  - python>=3.7
```

### 2. Install the package using `pip`

Before installing the package, make sure you have activated the conda environment you created in the previous step.
```bash
conda activate DataST
```

Then you can install the package using pip. There are two ways to do this:

To install the package in a conda environment, you can do the following
>- <code> pip install git+https://github.com/yaksilab/Javid_S2P_codes.git#subdirectory=DataST
 </code>

**Basic usage:**
in the terminal run the following command
```conda
python -m s2p_to_yaksi_datastructure /path/to/suite2p/data
```


### 3. Clone the repo <a id='clone'></a>
clone the repository local in your computer

>- <code> git clone https://github.com/yaksilab/Javid_S2P_codes/tree/main/DataST </code>

import the the module DataStructureTransform

>- <code> from s2p_to_yaksi_datastructure.DataStructureTransform import Transform_results  </code>

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

### 


  
