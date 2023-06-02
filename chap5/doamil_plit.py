from os import walk
pfam_boun={}
with  open('/media/shah/sdb/db/pfam_sql/pfamA_reg_full_significant.txt') as f:
    content_list = f.readlines()
    for x in content_list:
        line=x.split()
        pfam_boun[line[1]+'_'+line[2]]=line[3]+'_'+line[4]

f=[]
for (dirpath, dirnames, filenames) in walk('/media/shah/sdc/data/pfam_reloop_screen/'):
    f.extend(filenames)
    break

fasta=[]
for x in f:
    if x[-5:]=='fasta':
        fasta.append(x)

pfam_seq_tracker={}
pfam_list=[]
for x in fasta:
    with  open('/media/shah/sdc/data/pfam_reloop_screen/'+x) as f:
        content_list = f.readlines()
        line=content_list[0]
        line=line.rstrip()
        line=line.replace('>', '')
        a,b,c=line.split('_')
        pfam_list.append(b+'_'+c)
        pfam_seq_tracker[b]=c

cnt=0
pfam_domains_needed={}
for x in pfam_list:
    try:
        pfam_domains_needed[x]=pfam_boun[x]
    except:
        print(x)
        cnt+=1


f = open("./pfam_domains.txt", "w")
f.write("")
f2=open("./pfam_domains.txt", "a")
for x,y in pfam_domains_needed.items():
    f2.write(x+'\t'+y+'\n')

#print(pfam_domains_needed)
#print(cnt)

######################SWORD

sword_boun={}
f=[]
for (dirpath, dirnames, filenames) in walk('/media/shah/sdc/data/pfam_reloop_screen/pfam_models'):
    f.extend(filenames)
    break

sword=[]
for x in f:
    if x[-3:]=='txt':
        sword.append(x)

for x in sword:
    with  open('/media/shah/sdc/data/pfam_reloop_screen/pfam_models/'+x) as f:
        content_list = f.readlines()
        for y in content_list:
            if y[0:3]=='PDB':
                pdb=y[5:12]
                sword_boun[pdb]=[]

import re
delimiters = "\s", ";", " "
regexPattern = '|'.join(map(re.escape, delimiters))
for x in sword:
    with  open('/media/shah/sdc/data/pfam_reloop_screen/pfam_models/'+x) as f:
        content_list = f.readlines()
        for y in content_list:
            if y[0].isdecimal():
                temp_list=[]
                a,b,c,d,e,f=y.split('|')
                c=re.split(regexPattern, c)
                c=list(filter(None, c))
                temp_list.append(c)
                sword_boun[x[0:7]].append(temp_list)
                


final_sword_boun={}
for x,y in sword_boun.items():
    print(x[0:7])
    #print(pfam_seq_tracker[x[0:7]])
    try:
        pfam_id=x[0:7]+'_' +pfam_seq_tracker[x[0:7]] 
        final_sword_boun[pfam_id]=y
    except:
        cnt+=1
        print(x)

print(final_sword_boun)
print(len(final_sword_boun))

f = open("./sword_domains.txt", "w")
f.write("")
f2=open("./sword_domains.txt", "a")
for x,y in final_sword_boun.items():
    f2.write(x+'\t')
    for i in y:
        #f2.write('*')
        for j in y:
            for z in j:
             f2.write('*')
             #print(z)
             for k in z:
                 f2.write(k+'&')
    f2.write('\n')





