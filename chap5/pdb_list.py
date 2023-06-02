from os import walk
import shutil
import os

f = []
f_dic = {}
for (dirpath, dirnames, filenames) in walk('./'):
    f.extend(filenames)
    break

file_list=[]
for x in f:
    if x[-4:]=='.pdb':
        file_list.append(x[0:7])

print(file_list)
print(len(file_list))

