import subprocess
from os import walk
import os

f = []
for (dirpath, dirnames, filenames) in walk('./sequences'):
    f.extend(filenames)
    break

print(f)
print(len(f))

#for x in f:
    #os.mkdir(x[0:7])

cmd_list=[]

#for x in f:
    #cmd_list.append('csh /home/shah/progs/DMPfold/seq2maps.csh ' + '../sequences/' + x + ' > map_log.txt')
    #print(x)
    #cmd_list.append('find ./' + x[0:7] + ' ' + ' -ctime 0 -type f |xargs rm')
    #cmd_list.append('csh /home/shah/progs/DMPfold/2maps.csh' + '../sequences/' + x[0:7] + '.aln' + ' > map_log.txt')
    #cmd_list.append('ls -l ' + './' + x[0:7] + ' |grep "^-.*Apr 06" #|xargs rm')
    #cmd_list.append('/home/shah/progs/hmmer-3.2.1/easel/miniapps/esl-reformat a2m ./' + x[0:7] + '_metagenomics.sto > ./' + x[0:7] +'.a2m')
    #cmd_list.append('csh /home/shah/progs/DMPfold/aln2maps.csh ' + './' + x[0:7] + '.aln' + ' > map_log.txt')
#print(cmd_list)
#print(len(cmd_list))

#for x in cmd_list:
    #print(x)
    #directory = './' + (x[-25:-18])
    #print(directory)
    #subprocess.call(x, cwd = ('./' + x[-24:-17]) , shell=True)
    #subprocess.call(x, cwd = ('./' + x[-35:-28]) , shell=True)
    #subprocess.call(x, cwd = ('./' + x[-37:-30) , shell=True)
   # subprocess.call(x, cwd = ('./'+ x[-40:-33]) , shell=True)
   # subprocess.call(x, cwd = ('./' + x[-25:-18]) , shell=True)

cmd_list_2=[]
for x in f:
    cmd_list_2.append('/home/shah/progs/DMPfold/run_dmpfold.sh ' + '../sequences/' + x +  ' ./' + x[0:7] + '.21c' ' ./' + x[0:7] + '.map' ' ./' + x[0:7] + '_models' ' > model_log.txt &')

print(cmd_list_2)
print(len(cmd_list_2))

for x in cmd_list_2[0:]:
    print(x)
    directory = './' + (x[-32:-25])
    print(directory)
    subprocess.call(x, cwd = ('./' + x[-32:-25]) , shell=True)
