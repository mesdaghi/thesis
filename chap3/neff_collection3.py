import pandas as pd

neff_file = open('/media/shah/sdc/data/djr/nohup.out', 'r')
content = neff_file.readlines()

cnt=0
f = open('/media/shah/sdc/data/djr/neff.txt', 'w')


desired_lines = content[0:324:6]

for x in desired_lines:
    print(x)
    
pf_list=[]
for x in content[0:324:6]:
    pf=x[-12:-5]
    pf_list.append(pf)

neff_list=[]
for x in content[4:324:6]:
    neff=x
    neff=''.join(i for i in neff if i.isdigit())
    neff_list.append(neff)

print(pf_list)
print(neff_list)

df = pd.DataFrame()
df['pfam']  = pf_list
df['neff']  = neff_list

print(df)


df.to_csv(r'./neff.txt', header=None, index= None, sep =' ', mode='a')
    

