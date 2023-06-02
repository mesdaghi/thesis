temp_pdb_code = []
with open('/media/shah/sdc/data/re_loops/clans_all_clustered') as file:
    for line in file:
        temp_pdb_code.append(line)

pdb_code = []
for x in temp_pdb_code:
    a,b,c,d = x.split(':')
    pdb_code.append(a[0:4].upper())

for x in pdb_code:
    print(x)

reent_list=[]
with open('/media/shah/sdc/data/re_loops/for_shah.txt') as file:
    for line in file:
        line = line.strip('\n')
        reent_list.append(line)

reent_list_nr_details=[]
for x in pdb_code:
    for y in reent_list:
        if x==y[0:4]:
            reent_list_nr_details.append(y)

#reent_list_nr_details = list(dict.fromkeys(reent_list_nr_details))


for x in reent_list_nr_details:
     print(x)

