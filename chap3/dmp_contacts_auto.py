import os
from os import walk
import subprocess
import shutil


f = []
for (dirpath, dirnames, filenames) in walk('./sequences'):
    f.extend(filenames)
    break

print(f)
print(len(f))

#for x in f:
    #os.mkdir('./dmp/' + x[0:7])


#for x in f:
     #shutil.copy('/media/shah/sdc/data/dan/' + x[0:7] + '/' + x[0:7] + '.aln' ,'/media/shah/sdc/data/dan/dmp/' + x[0:7])
     #shutil.copy('/media/shah/sdc/data/dan/sequences/' +  x , '/media/shah/sdc/data/dan/dmp/' + x[0:7])
   # os.remove('/media/shah/sdc/data/dan/' + x[0:7] + '/' + x[0:7] + '.temp.mtx')
    #os.rename('/media/shah/sdc/data/dan/dmp/' + x[0:7] +  '/' + x , '/media/shah/sdc/data/dan/dmp/' + x[0:7] +  '/' + x[0:7] + '.fasta')


cmd_list=[]
for x in f:
    cmd = '~/progs/DeepMetaPSICOV/run_DMP.sh -i /media/shah/sdc/data/dan/dmp/' + x[0:7] + '/' + x[0:7] + '.fasta' + ' ' + '-a /media/shah/sdc/data/dan/dmp/' + x[0:7] + '/' + x[0:7] + '.aln'
    cmd_list.append(cmd)
    print(cmd)

for x in cmd_list:
    print(x)
    directory = './dmp/' + x[-11:-4]
    print(directory)
    subprocess.call(x, cwd = directory , shell=True)

