import subprocess
from os import walk
import os

f = []
for (dirpath, dirnames, filenames) in walk('./sequences'):
    f.extend(filenames)
    break

#print(f)
#print(len(f))

#for x in f:
 #   os.mkdir(x[0:7])

cmd_list=[]

for x in f:
    cmd = 'nohup /home/shah/progs/hmmer-3.2.1/src/jackhmmer -N 1 -A /media/shah/sdc/data/new/' + x[0:7] + '/'  + x[0:7] + '_metagenomics.sto --cpu 50 /media/shah/sdc/data/new/sequences/' + x +' ' +  '/media/shah/sdb/db/filtered_Eupathdb_SRC_MERC_Uniref100_MGnify_2.fasta > jhmmer_log.txt'
    cmd_list.append(cmd)
    print(cmd)

for x in cmd_list:
    print(x)
    directory = './' + (x[-167:-160])
    print(directory)
    subprocess.call(x, cwd = (directory) , shell=True)


