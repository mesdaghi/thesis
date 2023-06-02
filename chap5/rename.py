import os
from os import walk

f = []

for (dirpath, dirnames, filenames) in walk('./renamed'):
    f.extend(filenames)
    break

print(f)

track2={}
with open('./track_dali_all.txt', "r") as file:
    lines = file.readlines()
    for x in lines:
        a=x[0:4]
        b=(x[5:]).strip()
        track2[a]=b
print(track2)


for x in f:
    os.rename(x, './renamed/'+track2[x[0:4]]+'.pdb')
