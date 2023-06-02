from collections import Counter

f = open("./query.list", "r")

content = f.readlines()

print(len(content))

new_list_dic={}
for x in content:
    new_list_dic[x[0:4]]=x
######################################
count_pfam={}
for x in content:
    count_pfam[x]=x[0:4]

model_nos=list(count_pfam.values())
model_dic=dict.fromkeys(model_nos,0) 

print(model_dic)


#count={}
for x,y in count_pfam.items():
    for i,j in model_dic.items():
        if i==y:
            model_dic[i]+=1

cnt=0
for i,j in model_dic.items():
    if j>1:
        cnt+=1
        print(i + ' '+str(j))

print(cnt)



#tally=Counter(count_pfam)

#print(tally)
################################    

#print(new_list_dic)
print(len(new_list_dic))


#f2 = open("./query.list2", "w")

#for i,j in new_list_dic.items():
 #   f2.write(j)

