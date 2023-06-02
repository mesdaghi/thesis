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

pfam_list=[]
with open('./track.txt', "r") as file:
    lines = file.readlines()
    for x in lines:
        a,b=x.split('_')
        b=b.strip('\n')
        pfam_list.append(b)

#print(clans3)
#print(len(clans3))

cnt=0
for x in pfam_list:
    try:
        clan = clans[x]
        clans3[clan].append(x)
    except:
        cnt+=1

clans_copy=clans3.copy()

for x,y in clans_copy.items():
    if y==[]:
        clans3.pop(x)

print(clans3)
print(len(clans3))

cnt=0
for x,y in clans3.items():
    cnt = cnt+len(y)

print('No pfam seed seq that belong to clan '+ str(cnt))
