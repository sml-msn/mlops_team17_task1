import pandas as pd
import os
import datetime
from sys import argv

with open('loopCounter', 'r') as f:
  lineNum = int(f.readlines()[0])
  os.remove('loopCounter')

print('\n===============\nLOOP', lineNum+1, 'STARTED\n')
print('data creation started')

with open('data_urls.txt', 'r') as f:
  lines=f.readlines()
  urls = lines[lineNum].split(' , ')

try:
  os.mkdir('data')
except FileExistsError:
  print("...")

data = pd.read_csv(urls[0], encoding='latin-1', error_bad_lines=False)
target = pd.read_csv(urls[1])
newData = data.merge(target, how='inner', on='index')

trainDataFName = 'trainData_' + datetime.datetime.now().strftime("%d-%m-%y_%H-%M-%S") 
newData.to_csv(os.path.join('data',f'{trainDataFName}.csv'), index=False)
print('File created:', os.path.join('data',f'{trainDataFName}.csv'))

with open('buffer.txt', 'w+') as f:
  f.write(os.path.join('data',f'{trainDataFName}.csv'))

