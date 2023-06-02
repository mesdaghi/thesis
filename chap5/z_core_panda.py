import re
import pandas as pd
from bokeh.io import show
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.plotting import figure
from bokeh.plotting import figure, output_file, save
from bokeh.transform import factor_cmap
from bokeh.models import FactorRange
from bokeh.palettes import Spectral6
import numpy as np
from collections import Counter
import os
import shutil
import subprocess
import matplotlib.pyplot as plt
import seaborn as sns

cluster_result_file='./clust_6.txt'
cluster_number='cluster_test'
pdb_representative=''

track={}

with open('./track_dali_all.txt', "r") as file:
    lines = file.readlines()
    for x in lines:
        a=x[0:4]
        b=(x[5:]).strip()
        track[a]=b


matrix_data= []
with open('./ordered') as file:
    for line in file:
        line = line.split('\t')
        matrix_data.append(line)

clans_data={}
with open('./clan_track.txt', "r") as file2:
    lines = file2.readlines()
    for x in lines:
        a,b=x.split(' ')
        b=b.strip('\n')
        clans_data[a]=b


fields=[]
for x in matrix_data[1:]:
    pfam=track[x[0][0:4]]
    if pfam in clans_data.keys():
            fields.append(pfam +'#'+clans_data[pfam])
    else:
        fields.append(pfam +'#'+'NONE')

############check no of cry struct########
cry_list=[]
for x in fields:
    if x[12]=='#':
        cry_list.append(x)

print(cry_list)
print(len(cry_list))




####################################

data=[]
for x in matrix_data[1:]:
    temp_data=[]
    for y in x[1:]:
        y = y.strip()
        y = float(y)
        temp_data.append(y)
    data.append(temp_data)

df = pd.DataFrame(data, columns =fields, index=fields)
#print(df)
print(df.loc['PF00955_G3NFQ8_1_1169#CL0062','PF00955_4YZF#CL0062'])

################super of 0.1 score w/ corresponding cry model
intersect_ros=[]
intersect={'PF03083': '17.8', 'PF02116': '0.1', 'PF00523': '0.1', 'PF04608': '5.7', 'PF01027': '16.0', 'PF01062': '18.3', 'PF00324': '39.8', 'PF03839': '10.8', 'PF03253': '28.8', 'PF04882': '23.7', 'PF01124': '13.9', 'PF04756': '12.7', 'PF03062': '11.0', 'PF00864': '10.3', 'PF03188': '15.9', 'PF00209': '38.5', 'PF04588': '4.2', 'PF00230': '24.7', 'PF08016': '9.9', 'PF01148': '15.1', 'PF04547': '16.7', 'PF00953': '28.6', 'PF01151': '21.6', 'PF00858': '15.5', 'PF01529': '11.8', 'PF02673': '31.3', 'PF14798': '5.0', 'PF04143': '27.0', 'PF00375': '20.8', 'PF11847': '0.1', 'PF12534': '0.1', 'PF04193': '10.5', 'PF01956': '3.0', 'PF04142': '20.6', 'PF01569': '12.3', 'PF04678': '13.1', 'PF00029': '12.8', 'PF07264': '18.5', 'PF00520': '7.2', 'PF03189': '14.6', 'PF01184': '22.3', 'PF12740': '16.0', 'PF02133': '29.2', 'PF01496': '12.6', 'PF02163': '7.8', 'PF01312': '13.0', 'PF01435': '9.5', 'PF03023': '19.6', 'PF02453': '0.1', 'PF00873': '11.6', 'PF00813': '4.2', 'PF01545': '19.6', 'PF00876': '10.0', 'PF00664': '0.1', 'PF01864': '14.6', 'PF08627': '0.1', 'PF04103': '0.1', 'PF03611': '19.8', 'PF06963': '37.4', 'PF06781': '5.2', 'PF00909': '36.1', 'PF00822': '15.9', 'PF01554': '34.5', 'PF02683': '9.6', 'PF01769': '14.8', 'PF00893': '0.1', 'PF00115': '19.9', 'PF00223': '0.1', 'PF01252': '16.8', 'PF00810': '21.9', 'PF11894': '3.5', 'PF13520': '27.3', 'PF00939': '24.4', 'PF00654': '0.1', 'PF02293': '20.5', 'PF01790': '16.9', 'PF13727': '12.7', 'PF07884': '14.8', 'PF11658': '21.5', 'PF03030': '41.9', 'PF03176': '10.2', 'PF01544': '14.7', 'PF00122': '14.7', 'PF01490': '0.1', 'PF06109': '17.2', 'PF01786': '22.5', 'PF15110': '2.4', 'PF03458': '8.7', 'PF03348': '28.2', 'PF02628': '26.4', 'PF02386': '0.1', 'PF02096': '14.5', 'PF01036': '23.9', 'PF03647': '0.1', 'PF02544': '9.2', 'PF00854': '24.9', 'PF01235': '0.1', 'PF01040': '17.8', 'PF00001': '0.1', 'PF03155': '0.1', 'PF05879': '16.4', 'PF01061': '0.1', 'PF01699': '24.2', 'PF00902': '17.6', 'PF01891': '22.0', 'PF00916': '23.3', 'PF02516': '0.1', 'PF02949': '31.3', 'PF03185': '0.1', 'PF02660': '22.4', 'PF04973': '19.2', 'PF02632': '15.3', 'PF01758': '25.4', 'PF01733': '30.7', 'PF01618': '15.1', 'PF01219': '11.6', 'PF00474': '40.2', 'PF01454': '10.0', 'PF00119': '0.1', 'PF02460': '40.1', 'PF04109': '0.1', 'PF02517': '7.4', 'PF03006': '0.1', 'PF00487': '7.3', 'PF13347': '20.7', 'PF00335': '0.1', 'PF02028': '38.0', 'PF04888': '4.3', 'PF00083': '26.9', 'PF06965': '37.3', 'PF03806': '22.2', 'PF02600': '0.1', 'PF01694': '16.1', 'PF00860': '32.5', 'PF03595': '34.1', 'PF03552': '0.1', 'PF03213': '0.1', 'PF00955': '0.1', 'PF01566': '25.8', 'PF00999': '22.7', 'PF01222': '30.9', 'PF03073': '19.6', 'PF01080': '0.1', 'PF02233': '20.2', 'PF02535': '13.0', 'PF07095': '0.1', 'PF05241': '13.7', 'PF05569': '8.8', 'PF01384': '37.6', 'PF09387': '0.1', 'PF15009': '11.9', 'PF01098': '29.5', 'PF03151': '31.2', 'PF01226': '29.9', 'PF05197': '14.5', 'PF07885': '8.2', 'PF09819': '17.9', 'PF00771': '18.3', 'PF18415': '0.1', 'PF01066': '7.0', 'PF15122': '4.6'}

for x,y in intersect.items():
    if y=='0.1':
        intersect_ros.append(x)

intersect_af=[]
af_w_cry={'PF03083': '27.2', 'PF02116': '0.1', 'PF00523': '0.1', 'PF04608': '6.1', 'PF01027': '18.0', 'PF01062': '2.1', 'PF00324': '57.5', 'PF03839': '11.4', 'PF03253': '45.0', 'PF04882': '25.6', 'PF01124': '17.7', 'PF04756': '16.4', 'PF03062': '10.6', 'PF00864': '27.7', 'PF03188': '21.6', 'PF00209': '42.2', 'PF04588': '4.2', 'PF00230': '32.0', 'PF08016': '11.4', 'PF01148': '21.6', 'PF04547': '28.3', 'PF00953': '6.9', 'PF01151': '24.3', 'PF00858': '25.5', 'PF01529': '17.9', 'PF02673': '44.3', 'PF14798': '14.9', 'PF04143': '40.2', 'PF00375': '38.2', 'PF11847': '10.3', 'PF12534': '20.8', 'PF04193': '12.4', 'PF01956': '2.6', 'PF04142': '29.7', 'PF01569': '13.0', 'PF04678': '17.5', 'PF00029': '22.0', 'PF07264': '27.0', 'PF00520': '12.6', 'PF03189': '30.0', 'PF01184': '27.0', 'PF12740': '25.3', 'PF02133': '39.4', 'PF01496': '20.0', 'PF02163': '4.0', 'PF01312': '14.8', 'PF01435': '12.4', 'PF03023': '21.2', 'PF02453': '0.1', 'PF00873': '34.2', 'PF00813': '6.6', 'PF01545': '11.7', 'PF00876': '13.0', 'PF00664': '22.0', 'PF01864': '21.1', 'PF08627': '0.1', 'PF04103': '0.1', 'PF03611': '31.1', 'PF06963': '47.5', 'PF06781': '5.8', 'PF00909': '40.1', 'PF00822': '15.7', 'PF01554': '36.4', 'PF02683': '12.0', 'PF01769': '22.3', 'PF00893': '0.1', 'PF00115': '18.2', 'PF00223': '19.8', 'PF01252': '19.5', 'PF00810': '32.5', 'PF11894': '14.8', 'PF13520': '0.1', 'PF00939': '35.9', 'PF00654': '0.1', 'PF02293': '0.1', 'PF01790': '9.4', 'PF13727': '11.5', 'PF07884': '16.5', 'PF11658': '59.8', 'PF03030': '50.8', 'PF03176': '10.8', 'PF01544': '12.4', 'PF00122': '0.1', 'PF01490': '0.1', 'PF06109': '36.2', 'PF01786': '31.7', 'PF15110': '2.5', 'PF03458': '9.3', 'PF03348': '41.6', 'PF02628': '20.8', 'PF02386': '24.9', 'PF02096': '17.0', 'PF01036': '25.9', 'PF03647': '2.1', 'PF02544': '18.3', 'PF00854': '54.0', 'PF01235': '0.1', 'PF01040': '6.2', 'PF00001': '0.1', 'PF03155': '0.1', 'PF05879': '21.4', 'PF01061': '0.1', 'PF01699': '20.2', 'PF00902': '27.1', 'PF01891': '27.6', 'PF00916': '50.0', 'PF02516': '0.1', 'PF02949': '35.1', 'PF03185': '0.1', 'PF02660': '28.1', 'PF04973': '7.1', 'PF02632': '11.9', 'PF01758': '29.6', 'PF01733': '54.0', 'PF01618': '0.1', 'PF01219': '10.9', 'PF00474': '40.0', 'PF01454': '7.5', 'PF00119': '0.1', 'PF02460': '43.8', 'PF04109': '0.1', 'PF02517': '12.0', 'PF03006': '0.1', 'PF00487': '8.7', 'PF13347': '20.3', 'PF00335': '0.1', 'PF02028': '44.8', 'PF04888': '0.1', 'PF00083': '34.9', 'PF06965': '10.6', 'PF03806': '48.8', 'PF02600': '0.1', 'PF01694': '17.6', 'PF00860': '48.8', 'PF03595': '30.6', 'PF03552': '7.0', 'PF03213': '0.1', 'PF00955': '0.1', 'PF01566': '43.5', 'PF00999': '24.4', 'PF01222': '45.3', 'PF03073': '19.1', 'PF01080': '0.1', 'PF02233': '31.2', 'PF02535': '15.4', 'PF07095': '15.1', 'PF05241': '13.5', 'PF05569': '0.1', 'PF01384': '41.3', 'PF09387': '0.1', 'PF15009': '24.7', 'PF01098': '35.1', 'PF03151': '36.7', 'PF01226': '35.7', 'PF05197': '37.9', 'PF07885': '12.7', 'PF09819': '25.3', 'PF00771': '19.9', 'PF18415': '0.1', 'PF01066': '6.2', 'PF15122': '30.4'}


for x,y in af_w_cry.items():
    if y=='0.1':
        intersect_af.append(x)

cry_struct=[]
for x in fields:
    if x[0]=='P' and x[12]=='#':
        cry_struct.append(x)

af_struct=[]
for x in fields:
    if x[0]=='a':
        af_struct.append(x)

ros_struct=[]
for x in fields:
    if x[0]=='P' and x[12] !='#':
        ros_struct.append(x)

both_struggled=[]
for x in intersect_af:
    for y in intersect_ros:
        if x==y:
            both_struggled.append(x)

print(both_struggled)
print(len(both_struggled))

track2={}
with open('./track_dali_all.txt', "r") as file:
    lines = file.readlines()
    for x in lines:
        a=x[0:4]
        b=(x[5:]).strip()
        track2[b]=a


for x in intersect_af:
    for y in cry_struct:
        if x==y[0:7]:
            a,b = y.split('#')
            cry = track2[a]
            for i in af_struct:
                if x == i[3:10]:
                    a,b=i.split('#')
                    af=track2[a]
                    command="gesamt ./"+ cry +'.pdb ./'+ af +'.pdb -o ./poor_aln/'+'super_'+i+'XX'+y+".pdb"
                    #print(command)
               #     os.system(command)


for x in intersect_ros:
    for y in cry_struct:
        if x==y[0:7]:
            a,b = y.split('#')
            cry = track2[a]
            for i in ros_struct:
                if x == i[0:7]:
                    a,b=i.split('#')
                    ros=track2[a]
                    command="gesamt ./"+ cry +'.pdb ./'+ af +'.pdb -o ./poor_aln/'+'super_'+i+'XX'+y+".pdb"
                #    print(command)
              #      os.system(command)

for x in both_struggled:
    for y in cry_struct:
        if x==y[0:7]:
            a,b = y.split('#')
            cry = track2[a]
            for i in af_struct:
                if x == i[3:10]:
                    a,b=i.split('#')
                    af=track2[a]
                    for j in ros_struct:
                        if x == j[0:7]:
                            a,b=j.split('#')
                            ros=track2[a]
                            command="gesamt ./"+ cry +'.pdb ./'+ af +'.pdb ./'+ros+'.pdb -o ./poor_aln/'+'super3_'+i+'XX'+y+'XX'+j+".pdb"
                            #print(command)
             #               os.system(command)
                            print(i)






##############################################################


clus=[]
clans_in_clust=[]
unique_pfam=[]
clans_tally_unique={}
with open(cluster_result_file, "r") as file:
    lines = file.readlines()
    for x in lines:
        x=x.strip()
        clus.append(x)
        a,b=x.split('#')
        clans_in_clust.append(b)
        if a[0:2]=='af':
            i,j=a.split('_')
            unique_pfam.append(a[3:10])
        else:
            unique_pfam.append(a[0:7])
    clans_in_clust2 = dict.fromkeys(clans_in_clust,'')
    for c in lines:
        c=c.strip()
        for d,e in clans_in_clust2.items():
            if d=='NONE' and c[-4:]=='NONE':
                if c[0:2]=='af':
                 #   clans_in_clust2[d].append(c[3:10])
                    clans_in_clust2[d]=clans_in_clust2[d]+'#'+c[3:10]   
                else:
                 #   clans_in_clust2[d].append(c[0:7])
                    clans_in_clust2[d]=clans_in_clust2[d]+'#'+c[0:7]
            elif c[-6:]==d:
                if c[0:2]=='af':
                 #   clans_in_clust2[d].append(c[3:10])
                 clans_in_clust2[d]=clans_in_clust2[d]+'#'+c[3:10]
                else:
                 #   clans_in_clust2[d].append(c[0:7])
     #           clans_in_clust2[d].append(c)
                    clans_in_clust2[d]=clans_in_clust2[d]+'#'+c[0:7]

for x,y in clans_in_clust2.items():
    clans_in_clust2[x]=y.split('#')
for x,y in clans_in_clust2.items():    
    clans_in_clust2[x] = list(filter(None, y))
for x,y in clans_in_clust2.items():    
    clans_in_clust2[x] = list(dict.fromkeys(y))

print(clans_in_clust2)


list_of_lists = []
with open("/media/shah/sdb/db/pfam_sql/pfamA.txt", "r") as file:
    for line in file:
        line_list = line.split('\t')
        list_of_lists.append(line_list)

pfam_desc_dic = {}

for x in list_of_lists:
    pfam_desc_dic[x[0]] = x[3]+'_'+x[7]

clans_in_clust_desc={}
for x in clans_in_clust2['NONE']:
    clans_in_clust_desc[x]=pfam_desc_dic[x]


for x,y in clans_in_clust_desc.items():
    print(x+'\t'+y)


print('Size of cluster:'+str(len(unique_pfam)))
unique_pfam = list(dict.fromkeys(unique_pfam))
print('Unique pfams in cluster:'+str(len(unique_pfam)))
clans_in_clust_tally=Counter(clans_in_clust)
print('Tally of clans in cluster:'+str(clans_in_clust_tally))


for x,y in clans_in_clust2.items():
    print(x+' has ' +str(len(y))+' unique pfams')




no_in_actual_clan={}
clans={}
with open('/media/shah/sdb/db/pfam_sql/clan_membership.txt', "r") as file:
    lines = file.readlines()
    for x in lines:
        a,b=x.split('\t')
        b=b.strip('\n')
        clans[a]=[]
    for x in lines:
        a,b=x.split('\t')
        b=b.strip('\n')
        clans[a].append(b)
    for i,j in clans_in_clust2.items():
        for h,k in clans.items():
            if i!='NONE':
                no_in_actual_clan[i]=len(clans[i])
print('Number of members of query pfam clan: ')  
print(no_in_actual_clan)



###############gesamt
track2={}
with open('./track_dali_all.txt', "r") as file:
    lines = file.readlines()
    for x in lines:
        a=x[0:4]
        b=(x[5:]).strip()
        track[b]=a

list_of_none=[]
for x in clus:
    if x[-4:]=='NONE':
        list_of_none.append(x)

cluster_file=cluster_result_file
os.mkdir(cluster_file[2:9])
for x in clus:
    a,b=x.split('#')
    file_name='./'+track[a]+'.pdb'
    #####shutil.copyfile(pdb_representative, './'+cluster_file[2:8]+'/'+pdb_representative)
    shutil.copyfile(file_name, './'+cluster_file[2:9]+'/'+x+'.pdb')


for x in list_of_none:
    z_score=df.loc[x,pdb_representative]
    command="gesamt ./"+cluster_file[2:9]+"/"+ x +'.pdb ./'+cluster_file[2:9]+'/'+pdb_representative+'.pdb -o ./'+cluster_file[2:9]+'/'+'super_'+x+'_'+str(z_score)+".pdb"
    print(command)
    os.system(command)
#subprocess.call('gesamt ./'+cluster_file[2:8]+'/*.pdb -o ./'+cluster_file[2:8]+'/ges_output.pdb')
#os.system("cd ~")


dali_clus=[]
for x in clus:
    for y in clus:
        if x!=y:
            selection=df.loc[x,y]
            dali_clus.append(selection)

len_clust=len(dali_clus)

#print(dali_clus)
sorted_vals=sorted(dali_clus)
#print(sorted_vals)

################bokeh box plot
#https://stackoverflow.com/questions/42699306/why-is-bokeh-so-much-slower-than-matplotlib

df2 = pd.DataFrame()
df2['Vals'] = dali_clus
df2['Class'] = [cluster_number]*len_clust

#print(df2)
# find the quartiles and IQR for each category
groups = df2.groupby('Class')
q1 = groups.quantile(q=0.25)
q2 = groups.quantile(q=0.5)
q3 = groups.quantile(q=0.75)
iqr = q3 - q1
upper = q3 + 1.5*iqr
lower = q1 - 1.5*iqr

cluster = [cluster_number]

p = figure(x_range=cluster)

# if no outliers, shrink lengths of stems to be no longer than the minimums or maximums
qmin = groups.quantile(q=0.00)
qmax = groups.quantile(q=1.00)
upper.score = [max([x,y]) for (x,y) in zip(list(qmax.loc[:,'Vals']),upper.Vals)]
lower.score = [max([x,y]) for (x,y) in zip(list(qmin.loc[:,'Vals']),lower.Vals)]
#####column = df2["Vals"]
#####max_value = column.max()
#####min_value = column.min()
print(upper.score)
print(lower.score)

# stems
######p.segment(cluster, upper.Vals, cluster, q3.Vals, line_color="black")
#####p.segment(cluster, lower.Vals, cluster, q1.Vals, line_color="black")
p.segment(cluster, upper.score, cluster, q3.Vals, line_color="black")
p.segment(cluster, lower.score, cluster, q1.Vals, line_color="black")


# boxes
p.vbar(cluster, 0.7, q2.Vals, q3.Vals, fill_color="#E08E79", line_color="black")
p.vbar(cluster, 0.7, q1.Vals, q2.Vals, fill_color="#3B8686", line_color="black")

# whiskers (almost-0 height rects simpler than segments)
p.rect(cluster, lower.score, 0.2, 0.01, line_color="black")
p.rect(cluster, upper.score, 0.2, 0.01, line_color="black")

p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = "white"
p.grid.grid_line_width = 2
p.xaxis.major_label_text_font_size="12pt"

save(p)





################################## Violin plot
#data_to_plot = [dali_clus]
#fig, ax = plt.subplots()
#ax.set_title(cluster_number)
#ax.set_ylabel('Z- Score')
#####ax.xticklabels = ['Cluster 1']
#ax.yaxis.grid(True)
#plt.tick_params(
#    axis='x',          # changes apply to the x-axis
 #   which='both',      # both major and minor ticks are affected
  #  bottom=False,      # ticks along the bottom edge are off
   # top=False,         # ticks along the top edge are off
    #labelbottom=False) # labels along the bottom edge are off

# Create the boxplot
#bp = ax.violinplot(data_to_plot, showmedians=True)
#plt.savefig(cluster_number+'_vio.png')



###############seaborn vio plot  https://stackabuse.com/seaborn-violin-plot-tutorial-and-examples/
sns.set_palette("RdBu")
sns.set_style("darkgrid")
ax=sns.violinplot(x=dali_clus)
ax.set_title(cluster_number+" Z-Score Stats")
#ax.set_ylabel("Z-Score")
ax.set_xlabel("Z-Score")


######swarm
dali_clus_self_hits=[]
for x in clus:
    for y in clus:
        if x[0:2]=='af'and y[0:2]=='af':
            model1=(x[3:10])
            model2=(y[3:10])
        elif x[0:2]=='af'and y[0:2]!='af':
            model1=(x[3:10])
            model2=(y[0:7])
        elif x[0:2]!='af'and y[0:2]!='af':
            model1=(x[0:7])
            model2=(y[0:7])
        elif x[0:2]!='af'and y[0:2]=='af':
            model1=(x[0:7])
            model2=(y[3:10])
        if x!=y and model1==model2:
            selection=df.loc[x,y]
            dali_clus_self_hits.append(selection)

#print(dali_clus_self_hits)
    

sns.swarmplot(x=dali_clus_self_hits, color="k", alpha=0.8)




plt.savefig(cluster_number+'_seaborn_vio.png') 
