
import os
import glob
import json
import argparse
import warnings
import numpy as np
import pandas as pd
from scipy import spatial
from itertools import repeat
from biopandas.pdb import PandasPdb
from biopandas.mol2 import PandasMol2

warnings.filterwarnings("ignore", message = "Boolean Series key will be reindexed to match DataFrame index")

class FeatureGeneration():
    
    
    atom_types = {'OE1':'O','HB1':'H','SD':'S','HE':'H','1HD1':'H','1HG1':'H','2HD2':'H','1HD2':'H','CE3':'C','OH':'O','CZ':'C',
           'HG2':'H','HN2':'H','NZ':'N','HN1':'H','3HD2':'H','CD2':'C','2HH2':'H','HH2':'H','O':'O','2HD1':'H','ND1':'N',
           'HH':'H','1HE2':'H','HB':'H','NH2':'N','3HG1':'H','ND2':'N','CZ3':'C','HA2':'H','OG':'O','CG2':'C','CE':'C',
           'SG':'S','NE':'N','CG':'C','CB':'C','HG1':'H','NH1':'N','2HE2':'H','3HD1':'H','1HH2':'H','HD2':'H','HD1':'H',
           'NE1':'N','HB2':'H','HA':'H','3HG2':'H','HN3':'H','HE1':'H','CD':'C','HZ3':'H','OD1':'O','N':'N','H':'H',
           'HA1':'H','2HH1':'H','NE2':'N','CE2':'C','C':'C','OD2':'O','2HG1':'H','CD1':'C','HE3':'H','1HH1':'H','2HG2':'H',
           'HB3':'H','CE1':'C','OXT':'O','CH2':'C','1HG2':'H','HZ1':'H','OG1':'O','HZ2':'H','CA':'C','CG1':'C','HE2':'H',
           'CZ2':'C','OE2':'O','HG':'H','HZ':'H'}
    
    def __init__(self, directory,  
                 atoms_list , 
                 amino_acid_class_names,
                 amino_acid_class,
                 exp,
                 cutoff,
                 file_name):
        
        """Constructor to create an object for generating features with the given directory of structres which 
        every structures should be in a separate folder that contains mol2 file for ligand and pdb file for protein, 
        exponent(exp), distance cutoff(cutoff), different amino acid's classification(amino_acid_class) and 
        names(amino_acid_class_names), list of atoms(atoms_list) and file name(file_name) for saving features data into 
        an excel file"""
        
        self.directory = directory
        self.atoms_list = atoms_list
        self.amino_acid_class_names = amino_acid_class_names
        self.amino_acid_class = amino_acid_class
        self.exp = exp
        self.cutoff = cutoff
        self.file_name = file_name
        
    def _xyz_extract(self, arg, pdb_df):
        
        """Internal function for extracting atoms coordinates of proteins."""
        
        return list(map(lambda x: pdb_df.df['ATOM'][pdb_df.df['ATOM']['residue_name'].isin(arg)]
            [pdb_df.df['ATOM']['element_symbol'] == x][['x_coord','y_coord','z_coord']].values, self.atoms_list))
    
    def _distance_mat(self, i, xyz_ligand, xyz_protein):
        
        """Internal function for calculating distances between ligand and protein atoms"""
        
        return [np.round(sum(list(map(lambda m : 1./m**int(self.exp),filter(lambda n : n<int(self.cutoff),
            spatial.distance.cdist(xyz_ligand[x], xyz_protein[i][y]).ravel() )))),decimals = 2)
            for x in range(len(self.atoms_list)) for y in range(len(self.atoms_list))]
    
    def compute(self):
        
        """function is used for generating an excel file contains features which at first step 
        calculates distances between specified ligand atom type and protein atom type then rise 
        them individually to order one  (two or three). At the second stage inverses each term 
        and sums all terms together.  This process has been done for every combinations between 
        protein and ligand atom type"""
        
        protein_list = os.listdir(self.directory)
        
        if self.amino_acid_class_names == [] :
            
            atoms_combination = [i+j for i in self.atoms_list for j in self.atoms_list]
        
        else :
            
            atoms_combination = [k+i+j for k in self.amino_acid_class_names for i in self.atoms_list for j in self.atoms_list ]
            
        
        distance_df=pd.DataFrame(columns=atoms_combination)

        for i in range(len(protein_list)):
            
            mol2 = PandasMol2()
            
            pdb = PandasPdb()
            
            protein_folder = os.path.join(self.directory, protein_list[i])
            
            ligand_path = glob.glob(protein_folder+"\\"+"*.mol2")[0]

            protein_path = glob.glob(protein_folder+"\\"+"*.pdb")[0]
            
            mol2_df = mol2.read_mol2(ligand_path)
            
            mol2_df.df['element_symbol'] = mol2_df.df['atom_type'].apply(lambda x : x.split('.')[0])
            
            pdb_df = pdb.read_pdb(protein_path)
            
            pdb_df.df['ATOM']['element_symbol'] = pdb_df.df['ATOM']['atom_name'].map(self.atom_types)
            
            xyz_ligand = list(map(lambda x : mol2_df.df[mol2_df.df['element_symbol'] == x][['x','y','z']].values,
                                  self.atoms_list))
								
            if self.amino_acid_class_names == [] :
                
                
                xyz_protein = list(map(lambda x : pdb_df.df['ATOM'][pdb_df.df['ATOM']['element_symbol'] == x]
                                       [['x_coord','y_coord','z_coord']].values, self.atoms_list))
                
                mat = [np.round(sum(list(map(lambda m : 1./m**int(self.exp),filter(lambda n : n<int(self.cutoff) ,
                        spatial.distance.cdist(xyz_ligand[x],xyz_protein[y]).ravel() )))),decimals = 2) 
                        for x in range(len(self.atoms_list)) for y in range(len(self.atoms_list))]
            
            else : 
                
                xyz_protein = list(map(self._xyz_extract, self.amino_acid_class, repeat(pdb_df)))
            
                mat = np.array(list(map(self._distance_mat, range(0,len(self.amino_acid_class_names)), 
				repeat(xyz_ligand), repeat(xyz_protein)))).ravel()
            
            df = pd.DataFrame(data = np.array(mat).reshape(1,np.array(mat).shape[0]), columns = atoms_combination)
            
            distance_df = pd.concat([distance_df,df],axis=0)
                
        distance_df.index = os.listdir(self.directory)
        
        distance_df = distance_df.astype(float)
        
        distance_df = distance_df.loc[:, (distance_df != 0).any(axis=0)]
        
        return distance_df.to_excel(self.file_name)   

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description = "Generate features for set of given structures")
    parser.add_argument('-d',"--directory",  help = "directory of structures files", required = True)
    parser.add_argument('-a','--atoms_list', nargs="*", default=['H','C','N','O','S','P','F','Cl','Br','I'],
                       help = "list of atoms")
    parser.add_argument("-n","--amino_acid_class_names", nargs = "*", default = ['c','p','a','h'], 
                        help = " different classes of amino acids")
    parser.add_argument("-c","--amino_acid_class",
                        default = [['ARG', 'LYS', 'ASP', 'GLU'],
                        ['GLN', 'ASN', 'HIS', 'SER', 'THR', 'CYS'],
                        ['TRP','TYR','MET'],
                        ['ILE', 'LEU', 'PHE', 'VAL', 'PRO', 'GLY', 'ALA']] ,
                        help = "list of amino acids for each class", type=json.loads)
    parser.add_argument('-e', "--exp", type = int, default = 2, help = "exponent is used for wighting each invert distances")
    parser.add_argument('-o', "--cutoff", type = int, default = 12, help = "distance cutoff" )
    parser.add_argument('-f', "--file_name", default = "file.xlsx", help = "name of the generated file")
    
    args = parser.parse_args()
    
    
    for i in range(len(args.amino_acid_class)) :
        for j in range(len(args.amino_acid_class[i])) : 
            args.amino_acid_class[i][j]=str(args.amino_acid_class[i][j])
    
    feature=FeatureGeneration(directory = args.directory,  
                              atoms_list = args.atoms_list,
                              amino_acid_class_names = args.amino_acid_class_names, 
                              amino_acid_class = args.amino_acid_class, 
                              exp = args.exp, 
                              cutoff = args.cutoff, 
                              file_name = args.file_name)
    feature.compute()
