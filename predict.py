
import joblib
import argparse
import numpy as np
import pandas as pd
from generate_feature import FeatureGeneration

features = np.array(['cHH', 'cHC', 'cHN', 'cHO', 'cCH', 'cCC', 'cCN', 'cCO', 'cNH',
       'cNC', 'cNN', 'cNO', 'cOH', 'cOC', 'cON', 'cOO', 'cSH', 'cSC',
       'cSN', 'cSO', 'cPH', 'cPC', 'cPN', 'cPO', 'cFH', 'cFC', 'cFN',
       'cFO', 'cClH', 'cClC', 'cClN', 'cClO', 'cBrH', 'cBrC', 'cBrN',
       'cBrO', 'cIH', 'cIC', 'cIN', 'cIO', 'pHH', 'pHC', 'pHN', 'pHO',
       'pHS', 'pCH', 'pCC', 'pCN', 'pCO', 'pCS', 'pNH', 'pNC', 'pNN',
       'pNO', 'pNS', 'pOH', 'pOC', 'pON', 'pOO', 'pOS', 'pSH', 'pSC',
       'pSN', 'pSO', 'pSS', 'pPH', 'pPC', 'pPN', 'pPO', 'pPS', 'pFH',
       'pFC', 'pFN', 'pFO', 'pFS', 'pClH', 'pClC', 'pClN', 'pClO', 'pClS',
       'pBrH', 'pBrC', 'pBrN', 'pBrO', 'pBrS', 'pIH', 'pIC', 'pIN', 'pIO',
       'pIS', 'aHH', 'aHC', 'aHN', 'aHO', 'aHS', 'aCH', 'aCC', 'aCN',
       'aCO', 'aCS', 'aNH', 'aNC', 'aNN', 'aNO', 'aNS', 'aOH', 'aOC',
       'aON', 'aOO', 'aOS', 'aSH', 'aSC', 'aSN', 'aSO', 'aSS', 'aPH',
       'aPC', 'aPN', 'aPO', 'aPS', 'aFH', 'aFC', 'aFN', 'aFO', 'aFS',
       'aClH', 'aClC', 'aClN', 'aClO', 'aClS', 'aBrH', 'aBrC', 'aBrN',
       'aBrO', 'aBrS', 'aIH', 'aIC', 'aIN', 'aIO', 'aIS', 'hHH', 'hHC',
       'hHN', 'hHO', 'hCH', 'hCC', 'hCN', 'hCO', 'hNH', 'hNC', 'hNN',
       'hNO', 'hOH', 'hOC', 'hON', 'hOO', 'hSH', 'hSC', 'hSN', 'hSO',
       'hPH', 'hPC', 'hPN', 'hPO', 'hFH', 'hFC', 'hFN', 'hFO', 'hClH',
       'hClC', 'hClN', 'hClO', 'hBrH', 'hBrC', 'hBrN', 'hBrO', 'hIH',
       'hIC', 'hIN', 'hIO'], dtype=object)

atoms_list = ['H','C','N','O','S','P','F','Cl','Br','I']
amino_acid_class_names = ['c','p','a','h']
amino_acid_class = [['ARG', 'LYS', 'ASP', 'GLU'], ['GLN', 'ASN', 'HIS', 'SER', 'THR', 'CYS'], ['TRP','TYR','MET'],
                        ['ILE', 'LEU', 'PHE', 'VAL', 'PRO', 'GLY']]
exp = 2
cutoff = 12

if __name__ == "__main__":
    
    """Best trained model (et_model.sav) is used for predicting new samples. First it's used generate_feature 
    for generation of features for new samples then use them for predicting pKd"""
    
    parser = argparse.ArgumentParser(description = "Generate features for set of given structures")
    parser.add_argument('-m', '--model', help = 'path file of trained model', required = True)
    parser.add_argument('-d',"--directory",  help = "directory of structures files", required = True)
    parser.add_argument('-f', "--file_name", default = "features.xlsx", help = "name of the generated file")
    
    args = parser.parse_args()
    
    
    feature = FeatureGeneration(directory = args.directory,  
                              atoms_list = atoms_list,
                              amino_acid_class_names = amino_acid_class_names, 
                              amino_acid_class = amino_acid_class, 
                              exp = exp, 
                              cutoff = cutoff, 
                              file_name = args.file_name)
    feature.compute()
    
    model = joblib.load(args.model)
    data = pd.read_excel(feature.file_name, index_col = 0)
    empty_df = pd.DataFrame(columns = features)
    data = pd.concat([data, empty_df], axis = 0, sort = False).reindex(columns = features).fillna(value = 0.0)
    predict = model.predict(data)
    pd.DataFrame(data = predict, index = data.index, columns = ['prediction']).to_excel('prediction.xlsx')
