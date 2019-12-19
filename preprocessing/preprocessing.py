
from prody import *
import os
import glob
from openbabel import openbabel
import argparse

#Add Hydrogen atoms to pdb structure and separate ligand and protein and save them as .mol2 and .pdb respectively.

def extract_ligand(entry, path):
    pdb = parsePDB(entry.path)
    ligand = pdb.select('not protein and not water')
    molecule_pdb = path + entry.name[:-4] + '_ligand.pdb'
    writePDB(molecule_pdb, ligand)
    conversion = openbabel.OBConversion()
    conversion.SetInAndOutFormats("pdb", "mol2")
    mol = openbabel.OBMol()
    conversion.ReadFile(mol, molecule_pdb)
    mol.AddHydrogens()
    molecule_mol = path + entry.name[:-4] + '_ligand.mol2'
    conversion.WriteFile(mol, molecule_mol)
    
def extract_protein(entry, path):
    pdb = parsePDB(entry.path)
    protein = pdb.select('protein')
    molecule = path + entry.name[:-4] + '_protein.pdb'
    writePDB(molecule , protein)
    conversion = openbabel.OBConversion()
    conversion.SetInAndOutFormats("pdb", "pdb")
    mol = openbabel.OBMol()
    conversion.ReadFile(mol, molecule)
    mol.AddHydrogens()
    conversion.WriteFile(mol, molecule)
    
def extract(input_directory, output_directory):
    with os.scandir(input_directory) as entries:
        for entry in entries:
            path = output_directory + '\\output\\' + entry.name[:-4] + '\\'
            os.makedirs(path)
            extract_ligand(entry, path)
            extract_protein(entry, path)
            ligand_pdb = glob.glob(path + '*_ligand.pdb')
            os.remove(ligand_pdb[0])
            
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description = "Add Hydrogen atoms and separate ligand and protein")
    parser.add_argument("input_directory",  help = "Folder of complex structures in pdb format")
    parser.add_argument("output_directory", help = "Output directory")
    args = parser.parse_args()
    extract(args.input_directory, args.output_directory)
