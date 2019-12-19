### Tutorial for separating ligand and protein from *.pdb* complex file
   
   1- Installing open babel python :
      You can find instruction from [open babel site](https://open-babel.readthedocs.io/en/latest/UseTheLibrary/PythonInstall.html)
   
   2- Installing prody :
   ```
      pip install prody
   ```
   3- For using *preprocessing.py* all *.pdb* files should be in the same directory(*inputs_directory*) and
      output directory msut be determined(*output_directory*) :
   ```
      python preprocessing.py -h
	  python preprocessing.py inputs_directory output_directory
   ```