import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import os
from sklearn.metrics import mean_squared_error as mse
from sklearn.metrics import r2_score
from joblib import dump, load
import datetime
from sys import argv

print('model testing started')

with open('buffer.txt', 'r') as f:
  line = f.readlines()[0].split(' , ')
  modelPath = line[0]
  dfTestPath = line[1]

trn = pd.read_csv(dfTestPath)

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

model = load(modelPath) 
y_predict=model.predict(X)


print('\nОшибка на тестовых данных')
print('MSE: %.1f' % mse(y,y_predict))
print('RMSE: %.1f' % mse(y,y_predict,squared=False))
print('R2 : %.4f' %  r2_score(y,y_predict))

os.remove(os.getcwd() + '/buffer.txt')
