import re
import subprocess
from os import walk
import os

f = []
for (dirpath, dirnames, filenames) in walk('./sequences'):
    f.extend(filenames)
    break

cnt=0
log=[]
f_log = open("aln_check_log.txt", "w")
for x in f:
    print(x)
    with open('./' + x[0:7] + '/' + x[0:7] + '.aln') as myFile:
        text = myFile.read()
        text=text.splitlines()
        print(text[0:1])
        try:
            text.remove('')
        except:
            log.append(x)
            continue
        print(text[0:1])
        f = open('./' + x[0:7] + '/' + 'B' + x[1:7]+ '.aln', "w")
        for i in text:
            f.write(i+'\n')

for x in log:
    f_log.write(x + '\n')
f_log.write(str(len(log)))
f_log.close()
    

