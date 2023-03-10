import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import os
from sklearn.linear_model import Ridge
from joblib import dump, load
import datetime
from sys import argv

print('model preparation started')

with open('buffer.txt', 'r') as f:
  line = f.readlines()[0].split(' , ')
  dfTrainPath = line[0]
  dfTestPath = line[1]
  
trn = pd.read_csv(dfTrainPath)

cat_columns = []
num_columns = []

def CatNum(df, show = False):
  global cat_columns
  global num_columns
  cat_columns = []
  num_columns = []
  for column_name in df.columns:
      if (df[column_name].dtypes == object):
          cat_columns +=[column_name]
      else:
          num_columns +=[column_name]
  if show:
    print('Категориальные данные:\t ',cat_columns, '\n Число столблцов = ',len(cat_columns))
    print('Числовые данные:\t ',  num_columns, '\n Число столблцов = ',len(num_columns))
    print('=================\n')

CatNum(trn)
df_num = trn[num_columns].copy()

X,y = df_num.drop(columns = ['polution']).values,df_num['polution'].values

scaler  = MinMaxScaler()
scaler.fit_transform(X)
X = scaler.transform(X) 

print('model training')
model = Ridge()
model.fit(X, y)

try:
  os.mkdir('model')
except FileExistsError:
  print("...")
modelFName = 'model_' + datetime.datetime.now().strftime("%d-%m-%y_%H-%M-%S")
dump(model, os.path.join('model',f'{modelFName}.joblib')) 

print('\nFiles saved:')
print(os.path.join('model',f'{modelFName}.joblib'))

with open('buffer.txt', 'w') as f:
  text = os.path.join('model',f'{modelFName}.joblib') + ' , ' + dfTestPath
  f.write(text)
