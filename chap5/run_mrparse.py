from os import walk
import subprocess
import os

f=[]
for (dirpath, dirnames, filenames) in walk('/media/shah/sdc/data/pfam_reloop_screen/all_v_all/seq/'):
    f.extend(filenames)
    break

for x in f:
    subprocess.call('mrparse --seqin /media/shah/sdc/data/pfam_reloop_screen/all_v_all/seq/'+x, cwd = ('./') , shell=True)



