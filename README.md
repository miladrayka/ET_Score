# ET-Score
A scoring function based on Extra Trees algorithm for predicting ligand-protein binding affinity. PDBbind 2016v refined set minus core set is used for training ET-Score and core set is used as an independet test set. 
## Contact 
Milad Rayka, Chemistry and Chemical Engineering Research Center of Iran, milad.rayka@yahoo.com
...
...
## Citation
...
## Installation
Below package should be installed for using ET-Score.
Dependecies:

* python >= 3.7.0
* numpy 
* scipy
* pandas
* biopandas >= 0.2.4
* joblib
* scikit-learn  
  
For installing first make a virtual environment and activate it.  
  
On windows:                                                                                                                            
```
   python py -m venv env
   .\env\Scripts\activate
```
  
On macOS and Linux:                                                                                                                    
```
   python3 -m venv env
   source env/bin/activate
```
  
Which *env* is the location to create the virtual environment. Now you can install packages:   
```
   pip install *package_name*
```
## Usage
###1- Preparing ligand and protein file  

  a- Ligand and protein structure should be saved in .mol2 and .pdb format files respectively.  
  b- Each ligand and protein files for a specific complex must be placed in a same folder. 
  
###2- Generating features
