import os
import re

filename = "/home/shah/db/pdbtm/"
filename_pdb_nr = "/home/shah/db/pdbtm_nr_extract"
cnt = 0
cnt2 = 0
drug_list = []
drug_list_nr = []

for filename in os.listdir(filename):
    cnt += 1
    path = '/home/shah/db/pdbtm/' + filename
    fp = open(path)
    lines = fp.readlines()
    title = lines[1]
    title.upper()
    x = re.search('PROTON', title)
    if (x):
        cnt2 += 1
        filename = filename[0:4]
        drug_list.append(filename)
        print(filename)
        print(title)

    else:
        continue

for filename_pdb_nr in os.listdir(filename_pdb_nr):
    code = filename_pdb_nr[0:4]
    for y in drug_list:
        if y == code:
            drug_list_nr.append(y)



print(drug_list)
print(drug_list_nr)
percent = (cnt2/cnt)*100
print(cnt)
print(cnt2)
print(percent)


