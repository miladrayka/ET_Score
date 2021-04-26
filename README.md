# ET-Score
A scoring function based on Extra Trees algorithm for predicting ligand-protein binding affinity. PDBbind 2016v refined set minus core set is used for training ET-Score and core set is used as an independent test set. 

![alt text](https://github.com/miladrayka/ET_Score/blob/master/picture.tif)

## Contact 
Milad Rayka, Chemistry and Chemical Engineering Research Center of Iran, milad.rayka@yahoo.com

## Citation
...
## Installation
Below packages should be installed for using ET-Score.
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
### 1- Preparing ligand and protein file  

  a- Ligand and protein structure should be saved in *.mol2* and *.pdb* format files respectively.  
  b- Each ligand and protein files for a specific complex must be placed in a same folder.
  
  for example:  
  
  ``` 
      ./1a1e/1a1e_ligand.mol2
      ./1a1e/1a1e_protein.pdb
      ./1a4k/1a4k_ligand.mol2
      ./1a4k/1a4k_protein.pdb
  ```
### 2- Generating features  
  *generate_feature.py* is used for generating features of ET-Score:  
``` 
   python generate_feature.py -h  
   python generate_feature.py -d file_directory  
```
### 3- Training Random Forest(RF) of Extra Trees(ET) based on generated features
   *train_test.p* script is used for optimizing hyperparameters(*max_features*), training(both RF and ET) and predicting for a test set. -y flag lets the script to optimize hyperparameters.

``` 
   python train_test.py -h
   python train_test.py features_file.xlsx test_list_file.txt binding_affinity_file.xlsx -y True
```

### 4- Use a trained model for predicting pKd values for new samples
   If you don't want to train your model, you can simply use *et_score.sav* which is our best trained model or ET-Score. For doing thi  task *predict.py* should be used. 
   Hydrogens should be added to both ligands and proteins. 
    
 ``` 
    python predict.py -h
    python predict.py -m et_score.sav -d file_directory
    
``` 
   
