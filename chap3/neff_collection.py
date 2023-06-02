import subprocess
from os import walk
import os

f = []
for (dirpath, dirnames, filenames) in walk('./sequences'):
    f.extend(filenames)
    break

print(f)
print(len(f))


cmd_list=[]

for x in f:
    cmd_list.append('nohup conkit-msatool ./' + x[0:7] + '.aln jones ' + '>neff_info.txt')
#print(cmd_list)
#print(len(cmd_list))

neff_file = open("neff.txt", "w")
for x in cmd_list:
    print(x)
    directory = './' + (x[-32:-25])
    print(directory)
    try:
        subprocess.call(x, cwd = ('./' + x[-32:-25]) , shell=True)
        with open('./' + x[-32:-25] + '/' + 'neff_info.txt','r') as f2:
            content = f2.readlines()
            neff = content[4]
            neff=''.join(i for i in neff if i.isdigit())
            print(x[-32:-25] + ' ' + neff)
            neff_file.write(x[-32:-25] + ' ' + neff +'\n')
    except:
        neff_file.write(x[-32:-25] + ' ' + 'no .aln file' +'\n')


