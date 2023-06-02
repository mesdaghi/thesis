import re
import subprocess
import os

with open('./pdb_list.txt') as f:
    lines = f.read().splitlines() 
print(lines)

dali_query_db_cmds = []
for x in lines:
    dali_query_db_cmds.append('perl -I bin /home/shah/progs/DaliLite.v4/bin/import.pl' + ' ' + './' + x  + ' ' + x[0:4]  + ' ' + './DAT')

   # dali_query_db_cmds.append('perl -I bin /home/shah/progs/DaliLite.v4/bin/import.pl' + ' ' + x + ' ' + x[-8:-4] + ' ' + './DAT')

cnt=0
error=[]
for x in dali_query_db_cmds:
    print(x)
    try:
        if os.path.isfile('dali.lock'): 
            os.remove("dali.lock")
            cnt+=1
        subprocess.call(x, cwd  = './', shell=True)
    except:
        error.append(x)
        cnt+=1
        os.remove("dali.lock")

f = open('./query.list', "w")
for dirpath, subdirs, files in os.walk('./DAT'):
    for x in files:
        f.write(x[0:5] + '\n')

print(error)
print(cnt)
