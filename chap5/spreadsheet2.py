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

pfam_model_track={}
pfam_clans={}
with open('../track_dali_all.txt', "r") as file:
    lines = file.readlines()
    for x in lines:
        x=x.strip()
        x = x[0:4] + '-' + x[4+1: ]
        a,b=x.split('-')
        
        if b[0]=='P':
            pfam_id=b[0:7]
            #print(pfam_id)
        elif b[0]=='a':
            pfam_id=b[3:10]
        
        pfam_model_track[b]=pfam_id
        try:
            pfam_clans[b]=clans[pfam_id]
        except:
 #           print(pfam_id)
            continue
                

#print(pfam_clans)
#print(pfam_model_track)
f_clan = open("./clan_track.txt", "w")
for x,y in pfam_clans.items():
        f_clan.write(x+' '+y+'\n')

#####################write results
#cnt=[0,0,0,0,0,0,0,0]
#f = open("./results_z_more_5a.txt", "w")
#for x in dali:
#    list_of_lists = []
 #   with open(x, "r") as file:
  #      for line in file:
   #         stripped_line = line.strip()
    #        line_list = stripped_line.split()
     #       list_of_lists.append(line_list)
    #temp=[]
    #for y in list_of_lists:
     #   if len(y)>6:
      #      y.insert(len(y),'#')
       #     if y[7]=='MOLECULE:' or y[7]=='#':
        #        temp.append(y)
    #for z in temp:
     #   target=track[z[1][0:4]]
      #  query=track[x[2:6]]
       # pfam_target=pfam_model_track[target]
        #pfam_query=pfam_model_track[query]
#####        print(pfam_clans[pfam_query])
 #####       print(pfam_clans[pfam_target])
        
      #  if query in pfam_clans.keys() and target in pfam_clans.keys():
       #     if len(z)>8:
        #        description= z[8:(len(z)-1)]
         #       description=' '.join(map(str, description)) 
          #      if float(z[2])>5:
           #         f.write(track[x[2:6]]+'\t'+pfam_clans[query]+'\t'+z[0]+'\t'+track[z[1][0:4]]+'\t'+pfam_clans[target]+'\t'+z[2]+'\t'+z[3]+'\t'+z[4]+'\t'+z[5]+'\t'+z[6]+'\t'+description+'\n')
            #        cnt[0]+=1
            #else:
             #   if float(z[2])>5:
              #      f.write(track[x[2:6]]+'\t'+pfam_clans[query]+'\t'+z[0]+'\t'+track[z[1][0:4]]+'\t'+pfam_clans[target]+'\t'+z[2]+'\t'+z[3]+'\t'+z[4]+'\t'+z[5]+'\t'+z[6]+'\n')
               #     cnt[1]+=1
       # elif query in pfam_clans.keys() and target not in pfam_clans.keys():
        #    if len(z)>8:
         #       description= z[8:(len(z)-1)]
          #      description=' '.join(map(str, description))
           #     if float(z[2])>5:
            #        f.write(track[x[2:6]]+'\t'+pfam_clans[query]+'\t'+z[0]+'\t'+track[z[1][0:4]]+'\t'+'NONE'+'\t'+z[2]+'\t'+z[3]+'\t'+z[4]+'\t'+z[5]+'\t'+z[6]+'\t'+description+'\n')
             #       cnt[2]+=1
            #else:
             #   if float(z[2])>5:
              #      f.write(track[x[2:6]]+'\t'+pfam_clans[query]+'\t'+z[0]+'\t'+track[z[1][0:4]]+'\t'+'NONE'+'\t'+z[2]+'\t'+z[3]+'\t'+z[4]+'\t'+z[5]+'\t'+z[6]+'\n')
               #     cnt[3]+=1
        #elif query not in pfam_clans.keys() and target in pfam_clans.keys():
         #   if len(z)>8:
          #      description= z[8:(len(z)-1)]
           #     description=' '.join(map(str, description))
            #    if float(z[2])>5:
             #       f.write(track[x[2:6]]+'\t'+'NONE'+'\t'+z[0]+'\t'+track[z[1][0:4]]+'\t'+pfam_clans[target]+'\t'+z[2]+'\t'+z[3]+'\t'+z[4]+'\t'+z[5]+'\t'+z[6]+'\t'+description+'\n')
              #      cnt[4]+=1
            #else:
             #   if float(z[2])>5:
              #      print(target)
               #     print(pfam_target)
                #    f.write(track[x[2:6]]+'\t'+'NONE'+'\t'+z[0]+'\t'+track[z[1][0:4]]+'\t'+pfam_clans[target]+'\t'+z[2]+'\t'+z[3]+'\t'+z[4]+'\t'+z[5]+'\t'+z[6]+'\n')
                 #   cnt[5]+=1
        #elif query not in pfam_clans.keys() and target not in pfam_clans.keys():
         #   if len(z)>8:
          #      description= z[8:(len(z)-1)]
           #     description=' '.join(map(str, description))
            #    if float(z[2])>5:
             #       f.write(track[x[2:6]]+'\t'+'NONE'+'\t'+z[0]+'\t'+track[z[1][0:4]]+'\t'+'NONE'+'\t'+z[2]+'\t'+z[3]+'\t'+z[4]+'\t'+z[5]+'\t'+z[6]+'\t'+description+'\n')
              #      cnt[6]+=1
            #else:
             #   if float(z[2])>5:
              #      f.write(track[x[2:6]]+'\t'+'NONE'+'\t'+z[0]+'\t'+track[z[1][0:4]]+'\t'+'NONE'+'\t'+z[2]+'\t'+z[3]+'\t'+z[4]+'\t'+z[5]+'\t'+z[6]+'\n')
                   # cnt[7]+=1

#print(cnt)
