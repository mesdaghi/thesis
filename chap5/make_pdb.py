import re


window=list(range(330))

with open('./af_pf10136.pdb') as file:
    lines = file.readlines()
    pdb_data = [line.rstrip() for line in lines]


coord_data=[]
for z in pdb_data:
    z.split(' ')
    match = re.search('ATOM', z)
    if (match):
        coord_data.append(z)

pdb_file = []
for i in window:
    for res_number in coord_data:
        number = int(res_number[22:29].strip())
        if i == number:
            pdb_file.append(res_number)

with open('./selection' + '.pdb', "w") as f:
    for j in pdb_file:
        f.write(j + '\n')
            

