import os
import pandas as pd
from os import walk

f = []
for (dirpath, dirnames, filenames) in walk('/media/shah/sdc/data/dan/sequences'):
    f.extend(filenames)
    break

row_names = []
col_names = ['uniprot', 'meta_5', 'meta_1']

for x in f:
    row_names.append(x[0:7])

df_neff = pd.DataFrame(index=row_names, columns=col_names)

uniprot_file = open('/media/shah/sdc/data/dan/neff.txt','r')
content = uniprot_file.readlines()
neff_dic={}

for x in content:
    a,b = x.split(' ')
    neff_dic[a] = b

for key, value in neff_dic.items():
    df_neff.at[key, 'uniprot'] = int(value.strip())

print(df_neff)

