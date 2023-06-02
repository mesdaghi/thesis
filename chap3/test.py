import re

pdb_data=[]
with open('/media/shah/sdb/db/pdbtm_chain_split/3cxh_O.pdb') as file:
    for line in file:
        pdb_data.append(line.strip())

coord_data=[]
for x in pdb_data:
    x.split(' ')
    match = re.search('ATOM', x)
    if (match):
        coord_data.append(x)

for x in coord_data:
    print(x[23:28].strip())