## ET-Score
### Tutorial for predicting pKd of new samples by using ET-Score  

*predict.py* and *et_score.sav* need for this task.  
``` 
   python predict.py -m .\model\et_score.sav -d .\example\strutures\ 
```
-m flag is used for loading ET-Score and -d flag is detemining directory of our files. After finishing prediciton, file.xlsx and  
 prediction.xlsx are produced. file.xlsx contains features of all input structures and prediction.xlsx is predicted pKds for every      structures. 
