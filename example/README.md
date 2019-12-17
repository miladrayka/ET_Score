## ET-Score
###Tutorial for predicting pKd of new samples by using ET-Score  

*predict.py* and *et_model.sav* need for this task which *et_model.sav* is our saved scoring function or ET-Score.  
``` 
   python predict.py -m .\model\et_model.sav -d .\example\strutures\ 
```
-m flag is used for loading ET-Score and -d flag is detemining directory of our files. After finishing prediciton, file.xlsx and  
 prediction.xlsx are produced. file.xlsx contains features of all input structures and prediction.xlsx is predicted pKds for every      structures. 
