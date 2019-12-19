### Tutorial for separating ligand and protein from *.pdb* comlex file
   
   1- Installing openbabel python :
      Youou can find instruction from [openbabel site](https://open-babel.readthedocs.io/en/latest/UseTheLibrary/PythonInstall.html)
   
   2- Installing prody :
   ```
      pip install prody
   ```
   3- For using *preprocessing.py* all *.pdb* files should be in the same directory(*inputs_directory*) and
      output directory msut be determined(*output_directory*) :
   ```
      python preprocessing.py -h
	  python preprocessing.py inputs_directory output_directory