import subprocess
import datetime

lineList = [line.rstrip('\n') for line in open('/media/shah/sdb/db/pdb_update.logs')]

cmd_list=[]

for x in lineList:
    if x[-3:] == '.gz' and x[0:3] != 'del':
        cmd = 'perl -I bin /home/shah/progs/DaliLite.v4/bin/import.pl' + ' ' +  '/media/shah/sdb/db/pdb/' + x + ' ' + x[-11:-7]  + ' ./DAT_pdb/'
        cmd_list.append(cmd)

for x in cmd_list:
    print(x)
    subprocess.call(x, cwd = ('./') , shell=True)



now = datetime.datetime.now()
print ("Dali db update on :")
print (str(now))


