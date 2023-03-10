import pandas as pd
from sklearn.model_selection import train_test_split
import os
import datetime
from sys import argv

print('preprocessing started')

with open('buffer.txt', 'r') as f:
  trainDataPath = f.readlines()[0]

print(trainDataPath)
trn = pd.read_csv('data/trainData.csv')

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
    
print('drop duplicates')
trn = trn.drop_duplicates()
trn = trn.drop_duplicates(['polution'])

print('drop boundary values')
question_dist = trn[trn.polution < 10e-2] 
trn = trn.drop(question_dist.index)
question_dist = trn[trn.polution > 2.5] 
trn = trn.drop(question_dist.index)

CatNum(trn)
print('drop waste columns')
waste = ['index', 'period', 'tourists', 'venue', 'rate', 'food', 'glass', 'metal', 'other', 'paper', 'plastic', 'leather', 'green_waste', 'waste_recycling']
trn = trn.drop(columns=waste)
CatNum(trn)

print('''OHE columns: code, year, Country, id''')
trn = pd.get_dummies(trn, columns=['code', 'year', 'Country'], drop_first= False)
trn = pd.get_dummies(trn, columns=['id'], drop_first= False)
CatNum(trn)

df_train, df_test = train_test_split(trn.dropna(), test_size=0.2, random_state=42)

try:
  os.mkdir('train')
except FileExistsError:
  print("...")
trainFName = 'df_train_' + datetime.datetime.now().strftime("%d-%m-%y_%H-%M-%S")
df_train.to_csv(os.path.join('train',f'{trainFName}.csv'))

try:
  os.mkdir('test')
except FileExistsError:
  print("...")
testFName = 'df_test_' + datetime.datetime.now().strftime("%d-%m-%y_%H-%M-%S")
df_test.to_csv(os.path.join('test',f'{testFName}.csv'))


print('\nFiles saved:')
print(os.path.join('train',f'{trainFName}.csv'))
print(os.path.join('test',f'{testFName}.csv'))

with open('buffer.txt', 'w') as f:
  text = os.path.join('train',f'{trainFName}.csv') + ' , ' + os.path.join('test',f'{testFName}.csv')
  f.write(text)

