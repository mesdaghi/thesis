import os
from os import walk
import operator
import shutil

f = []
f_dic = {}
for (dirpath, dirnames, filenames) in walk('./dali'):
    f.extend(filenames)
    break

print(f)


cnt=1000
track = {}
for x in f:
    cnt += 1
    a,b=x.split('.')
    track[str(cnt)]= a
    shutil.copyfile('./dali/' + x,
                    './dali_all/'  + str(cnt) + '.pdb')
print(track)

file = open("track_dali_all.txt", "w")
for x,y in track.items():
    file.write(x+'_'+y+'\n')
