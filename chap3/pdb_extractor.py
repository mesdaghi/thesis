import os
import re
from shutil import copyfile

filename_root = "/media/shah/sdb/db/pdbtm/"
query = 'ABC'
filename_fasta = "/media/shah/sdb/db/pdbtm_fasta/"
extracted_data_dir = '/media/shah/sdc/data/abc_screen/'


cnt = 0
cnt2 = 0
pdb_list = []

for filename in os.listdir(filename_root):
    cnt += 1
    path = filename_root + filename
    fp = open(path)
    lines = fp.readlines()
    title = lines[1]
    title.upper()
    x = re.search(query, title)
    if (x):
        cnt2 += 1
        filename = filename[0:4]
        pdb_list.append(filename)
print('total pdb files = ' + str(cnt))
print('total query pdb files = ' + str(cnt2))

os.mkdir(extracted_data_dir)

for x in pdb_list:
    print(filename_fasta + x + '.fasta.txt')
    try:
        copyfile(filename_fasta + x + '.fasta.txt', extracted_data_dir)
    except:
        x = x.upper()
        copyfile(filename_fasta + x + '.fasta.txt', extracted_data_dir + x + '.fasta.txt')

