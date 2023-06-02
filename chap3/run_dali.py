from os import walk
import subprocess
import os

f = []
for (dirpath, dirnames, filenames) in walk('./sequences'):
    f.extend(filenames)
    break

target_list = []
for (dirpath, dirnames, filenames) in walk('/home/shah/progs/DaliLite.v4/DAT_pdb'):
    target_list.extend(filenames)
    break

file = open("/home/shah/progs/DaliLite.v4/target.list", "w")
for x in target_list:
    file.write(x[0:5] + '\n')
file.close()


for x in f:
    #os.mkdir('./' + x[0:7] + '/dali')
    #os.mkdir('./' + x[0:7] + '/dali' + '/DAT')
    file = open('./' + x[0:7] + '/dali' + '/query.list', "w")
    file.write('finaA')
    file.close()
    if os.path.exists("dali.lock"):
        os.remove("dali.lock")
    cmd1 = 'perl -I bin /home/shah/progs/DaliLite.v4/bin/import.pl' + ' ' + './' + x[0:7] + '/' + x[0:7] + '_models/' + 'final_1.pdb' + ' ' + 'fina' + ' ' + './' + x[0:7] +  '/dali/DAT/'
    if os.path.exists('./' + x[0:7] + '/' + x[0:7] + '_models/' + 'final_1.pdb'):
        print(cmd1)
        subprocess.call(cmd1, cwd = ('./') , shell=True)


##############need to serialise with &
for x in f[51:]:
    print(x)
    cmd2 = 'perl -I bin /home/shah/progs/DaliLite.v4/bin/dali.pl --query ' + '/media/shah/sdc/data/dan/' + x[0:7] + '/dali' + '/query.list ' + '--db ' + '/home/shah/progs/DaliLite.v4/target.list ' + '--dat1 ' + '/media/shah/sdc/data/dan/' + x[0:7] + '/dali' + '/DAT ' + '--dat2 '  + '/home/shah/progs/DaliLite.v4/DAT_pdb &'
    print(cmd2)
    if os.path.exists('./' + x[0:7] + '/' + x[0:7] + '_models/' + 'final_1.pdb'):
        subprocess.call(cmd2, cwd = ('./' + x[0:7] + '/dali') , shell=True)
