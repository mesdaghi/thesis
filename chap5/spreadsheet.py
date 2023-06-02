from os import walk


f = []
f_dic = {}
for (dirpath, dirnames, filenames) in walk('./'):
    f.extend(filenames)
    break

dali=[]
for x in f:
    if x[-4:] == '.txt':
        y='./'+x
        dali.append(y)


track={}

with open('../track_dali_all.txt', "r") as file:
    lines = file.readlines()
    for x in lines:
        x=x.strip()
        x = x[0:4] + '-' + x[4+1: ]
        a,b=x.split('-')
        track[a]=b

#############clans
clans={}
with open('/media/shah/sdb/db/pfam_sql/clan_membership.txt', "r") as file:
    lines = file.readlines()
    for x in lines:
        a,b=x.split('\t')
        b=b.strip('\n')
        clans[b]=a
#print(clans)


clans2={}
with open('/media/shah/sdb/db/pfam_sql/clan_membership.txt', "r") as file:
    lines = file.readlines()
    for x in lines:
        a,b=x.split('\t')
        b=b.strip('\n')
        clans2[a]=b

clans3={}
with open('/media/shah/sdb/db/pfam_sql/clan_membership.txt', "r") as file:
    lines = file.readlines()
    for x in lines:
        a,b=x.split('\t')
        b=b.strip('\n')
        clans3[a]=[]

pfam_clans={}
with open('../track_dali_all.txt', "r") as file:
    lines = file.readlines()
    for x in lines:
        x=x.strip()
        x = x[0:4] + '-' + x[4+1: ]
        a,b=x.split('-')
        
        if b[0]=='P':
            pfam_id=b[0:7]
            print(pfam_id)
        elif b[0]=='a':
            pfam_id=b[3:10]
        
        try:
            pfam_clans[b]=clans[pfam_id]
        except:
            print(pfam_id)
                

#print(pfam_clans)


#####################write results
f = open("./results_z_more_5a.txt", "w")
for x in dali:
    list_of_lists = []
    with open(x, "r") as file:
        for line in file:
            stripped_line = line.strip()
            line_list = stripped_line.split()
            list_of_lists.append(line_list)
    temp=[]
    for y in list_of_lists:
        if len(y)>6:
            y.insert(len(y),'#')
            if y[7]=='MOLECULE:' or y[7]=='#':
                temp.append(y)
    for z in temp:
        if len(z)>7:
            description= z[8:(len(z)-1)]
            description=' '.join(map(str, description)) 
            if float(z[2])>5:
                    f.write(track[x[2:6]]+'\t'+pfam_clans[x[2:6]]+'\t'+z[0]+'\t'+track[z[1][0:4]]+'\t'+pfam_clans[z[1][0:4]]+'\t'+z[2]+'\t'+z[3]+'\t'+z[4]+'\t'+z[5]+'\t'+z[6]+'\t'+description+'\n')
        else:
            if float(z[2])>5:
                f.write(track[x[2:6]]+'\t'+pfam_clans[x[2:6]]+'\t'+z[0]+'\t'+track[z[1][0:4]]+'/t'+pfam_clans[z[1][0:4]]+'\t'+z[2]+'\t'+z[3]+'\t'+z[4]+'\t'+z[5]+'\t'+z[6])

