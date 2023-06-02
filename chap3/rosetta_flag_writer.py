import random
import subprocess
import os
import time
from collections import Counter
import datetime
import re



########################variables################################
#flag file called 'flag_membrane' is required in 'root' directory
split_job_into = 50
name_prot_dir = 'tmem41b'
root_path = '/media/shah/sdc/data/tmem41b/rosetta_membrane/'
flags_path = '/media/shah/sdc/data/tmem41b/rosetta_membrane/flags_membrane'
command = "/home/shah/progs/rosetta_src_2018.33.60351_bundle/main/source/bin/membrane_abinitio2.linuxgccrelease @  "
#################################################################


print('*********************making dirs & flag files*****************************')

l = []
l.extend(range(1, (split_job_into + 1)))
l = [str(x) for x in l]
l = ["G" + x for x in l]
protein_name_length = len(name_prot_dir)
print(l)

new_root = root_path + 'rosetta_models/'
os.mkdir(new_root)

#root_path = new_root

for folder in l:
    os.mkdir(os.path.join(new_root,folder))

with open (flags_path) as f:
    flags = f.readlines()
    print(flags)

cmds_list = []
for root, dirs, files in os.walk(new_root, topdown=False):
    for name in dirs:
        seed = str(random.randint(-2 ** 31, 2 ** 31))
        with open(os.path.join(root,name,'flags_membrane.txt'), 'w') as f:
            for x in flags:
                print(x)
                f.write(x)
            f.write('-run:jran ' + seed)
        w_dir = new_root + name
        cmds_list.append([command + new_root + name + '/flags_membrane.txt > rosetta.log &'])

length_cmds_list = len(cmds_list)

#executes rosetta for all directories created (apart from first directory) '&' execution in background preventing 'hangup' allowing for loop to complete
print('************Making Models****************************************')
for cmd in cmds_list[1:length_cmds_list]:
    print(cmd)
    subprocess.call(cmd, cwd = ((cmd[0])[104:(161+protein_name_length)]) , shell=True)

time.sleep(3600)    #time gap of 60mins before moving on to last set of models in foreground

#executes rosetta for first directory. Not sent to background, creating hangup before the rest of script executed ie time given before all models collected into single directory
print('************Making last set of models****************************')
for cmd in cmds_list[0]:
    subprocess.call((cmd[0:(193+protein_name_length)]), cwd=(cmd[104:(161+protein_name_length)]), shell=True)

#all models collected into single dir
print('************collect all models into single directory****************************')
for cmd in cmds_list[0]:
    models_dir = (cmd[104:(143+protein_name_length)]) + 'models/'
    os.mkdir(models_dir)  # make new dir to place all models into
    n = 1
    pdb_files = []

    for dirpath, subdirs, files in os.walk(new_root):
        for x in files:
            if x.endswith(".pdb"):
                pdb_files.append(os.path.join(dirpath, x))

    print('************printing info for log****************************')
#info printed for log
    print(pdb_files)

    dirs = []
    for x in pdb_files:
        dirs.append(x[54 + protein_name_length:57 + protein_name_length])

    dirs2 = []
    for x in dirs:
        a = (x.replace('/', ''))
        dirs2.append(a)

    tally = Counter(dirs2)

    print('Number of models made ' + '(' + str(datetime.datetime.now()) + ')' + ':' + (str(sum(tally.values()))))

    print(tally)

    for file in pdb_files:
        os.rename(file, (models_dir + 'model_' + '{n}'.format(n=n) + '.pdb'))
        n+=1

print('************performing spicker clustering****************************')

subprocess.call('ccp4-python ~/progs/destination/ccp4-7.0/lib/py2/ample/util/spicker.py -e ~/progs/destination/ccp4-7.0/bin/spicker -m ./models/ -t 50 > spicker_log.txt', cwd = root_path, shell=True)

print('************constructing Dali input files****************************')



dali_root = root_path + 'dali/'
os.mkdir(dali_root)

query_db_dir = dali_root + 'DAT/'
os.mkdir(query_db_dir)

paths =[]
with open(root_path + 'spicker_log.txt') as file:
    for line in file:
        line = [line.rstrip()]
        #print(line)
        path = line[0]
        x = re.search('centroid', path)
        if (x):
            paths.append(path[21:])
            print(path[21:])

root_path_len = len(root_path)
with open(root_path + 'pdb_list.txt', 'w') as file:
    for p in paths:
        file.write('../models/' + p[root_path_len+7:] + '\n')

with open(root_path + 'pdb_list.txt') as f:
    lines = f.read().splitlines()
print(lines)

dali_query_db_cmds = []
for x in lines:
    print(x)
    dali_query_db_cmds.append('perl -I bin /home/shah/progs/DaliLite.v4/bin/import.pl' + ' ' + x + ' ' + x[-8:-4] + ' ' + './DAT')

for x in dali_query_db_cmds:
    print(x)
    subprocess.call(x, cwd = './dali', shell=True)

f = open('./dali/query.list', "w")
for dirpath, subdirs, files in os.walk('./dali/DAT'):
    for x in files:
        f.write(x[0:5] + '\n')


print('************performing Dali alignments****************************')

subprocess.call('perl -I bin /home/shah/progs/DaliLite.v4/bin/dali.pl --query ./query.list --db /home/shah/progs/DaliLite.v4/target.list --dat1 ./DAT --dat2 /home/shah/progs/DaliLite.v4/DAT/', cwd = './dali', shell=True)



print('done!')





