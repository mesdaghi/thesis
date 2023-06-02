import pandas as pd
from bokeh.io import show
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.plotting import figure
from bokeh.plotting import figure, output_file, save
from bokeh.transform import factor_cmap
from bokeh.models import FactorRange
from bokeh.palettes import Spectral6

model_dic={}
with open('./track_dali_all.txt', "r") as file:
    lines = file.readlines()
    for x in lines:
        b=(x[5:]).strip()
        a=x[0:4]
        model_dic[a]=b

###############h score track

hscore_dic={}
with open('./h_score_track.txt', "r") as file:
    lines = file.readlines()
    for x in lines:
        a,b=x.split(' ')
        hscore_dic[a]=float(b.strip())

print(hscore_dic)
print(len(hscore_dic))
#####################get crystal pf names
crystal_dic={}
for x,y in model_dic.items():
    temp=y.split('_')
    if len(temp[1])==4:
        crystal_dic[x]=temp[0]
print(str(len(crystal_dic)) + ' crystals')
#################3get dic of af models
af_dic={}
for x,y in model_dic.items():
    temp=y.split('_')
    if temp[0]=='af': 
        af_dic[temp[1]]=x+'_'+y
print(str(len(af_dic)) + ' af')
####################get corresponding af model names
cry_w_af_dic={}
for x,y in crystal_dic.items():
    if y in af_dic:
        af_model=af_dic[y].split('_')
        cry_w_af_dic[af_model[2]]=x+'_'+af_model[0]
print(str(len(cry_w_af_dic))+' af models with crystal')

##################get dic of trros models
ros_dic={}
for x,y in model_dic.items():
    temp=y.split('_')
    #print(temp[1][0:1])
    if len(temp[1])>4 and temp[1][0:2]!='PF':
        ros_dic[temp[0]]=x+'_'+y
print(str(len(ros_dic)) + ' ros')
#print(ros_dic)

#########################get corresponding ros model names
cry_w_ros_dic={}
for x,y in crystal_dic.items():
    if y in ros_dic:
        ros_model=ros_dic[y].split('_')
        #print(ros_model)
        #cry_w_ros_dic[x]=ros_model[0]
        cry_w_ros_dic[ros_model[1]]=x+'_'+ros_model[0]

#print(cry_w_ros_dic)
print(str(len(cry_w_ros_dic))+' ros models with crystal')

####################df for dali data

matrix_data= []
model_code=[]
with open('./ordered') as file:
    for line in file:
        line=line.strip()
        line = line.split('\t')
        matrix_data.append(line[1:])
        model_code.append(line[0][0:4])
del matrix_data[0]
del model_code[0]
#print(len(model_code))
#print(len(matrix_data))

df = pd.DataFrame(matrix_data, columns =model_code, index=model_code)

##################update with missing values














#############################################




print(df)
#cell_test=df.loc['3201A','3201A']
#print(cell_test)

####################dic for af dali results w/ crystal
cnt=0
af_dali={}
for x,y in cry_w_af_dic.items():
    try:
        a,b=y.split('_')
        dali=df.loc[a,b]
        af_dali[x]=dali
    except:
        cnt+=1
print('***************')
print(af_dali)
#print(len(af_dali))
print(str(cnt)+' number of af dali not porcessed')

####################dic for af ros results w/ crystal
cnt=0
ros_dali={}
for x,y in cry_w_ros_dic.items():
    try:
        a,b=y.split('_')
        dali=df.loc[a,b]
        ros_dali[x]=dali
    except:
        cnt+=1

#print(ros_dali)
#print(len(ros_dali))
print(str(cnt)+' number of ros dali not porcessed')

##############intersect of pdb, df & ros
final_ros={}
for x,y in af_dali.items():
    final_ros[x]=ros_dali[x]

print('###################')
print(final_ros)
print(len(final_ros))

##################plot
pfams=[]
for x,y in final_ros.items():
    pfams.append(x)

trRosetta=list(final_ros.values())
#print(trRosetta)

pfams = pfams
methods = ['trRosetta', 'AF']

data = {'Pfam' : pfams,
        'trRosetta'   : list(final_ros.values()),
        'AF'   : list(af_dali.values())}

# this creates [ ("Apples", "2015"), ("Apples", "2016"), ("Apples", "2017"), ("Pears", "2015), ... ]
x = [ (pfam, method) for pfam in pfams for method in methods ]
counts = sum(zip(data['trRosetta'], data['AF']), ()) # like an hstack

source = ColumnDataSource(data=dict(x=x, counts=counts))

p = figure(x_range=FactorRange(*x), plot_height=250, title="PDB Alignment Dali Z Scores for tr Rosetta and AF Models",
           toolbar_location=None, tools="")

p.vbar(x='x', top='counts', width=0.9, fill_color=factor_cmap('x', palette=["#c9d9d3", "#718dbf"], factors=methods, start=0),source=source)
#p.vbar(x='x', top='counts', width=0.9, color='color' ,source=source)


p.y_range.start = 0
p.x_range.range_padding = 0.1
p.xaxis.major_label_orientation = 1
p.xgrid.grid_line_color = None

#save(p)


##############matplotlib

#import matplotlib.pyplot as plt
#import numpy as np


#labels = pfams
#men_means = list(final_ros.values())
#women_means = list(af_dali.values())

#print(women_means)

#x = np.arange(len(labels))  # the label locations
#width = 0.5  # the width of the bars

#fig, ax = plt.subplots()
#rects1 = ax.bar(x - width, men_means, width, label='Ros')
#rects2 = ax.bar(x + width, women_means, width, label='AF')

# Add some text for labels, title and custom x-axis tick labels, etc.
#ax.set_ylabel('Z Score')
#ax.set_title('Scores by Pfam and method')
#ax.set_xticks(x)
#ax.set_xticklabels(labels)
#ax.legend()

#ax.bar_label(rects1, padding=3)
#ax.bar_label(rects2, padding=3)

#fig.tight_layout()

#plt.savefig('z_comparison.png')
df2 = pd.DataFrame(columns=['pfam','ros', 'AF'])


###find how many times trros out performed af
cnt=0
for x, y in final_ros.items():
    if float(y)>float(af_dali[x]):
        cnt+=1
print('trros out performed af ' + str(cnt))

cnt=0
for x, y in final_ros.items():
    if float(y)==0.1:
        cnt+=1
print('trros w/ z score 0.1 ' + str(cnt))

cnt=0
hscore_log={}
hscore_log2={}
for x, y in af_dali.items():
    if float(y)==0.1:
        cnt+=1
        hscore_log[x]=hscore_dic[x]
    else:
        hscore_log2[x]=hscore_dic[x]

print('AF w/ z score 0.1 ' + str(cnt))
print(hscore_log)

mean_hscore1=sum(list(hscore_log.values()))/len(list(hscore_log.values()))
print('mean hscore for af models with 0.1 z score'+str(mean_hscore1))

mean_hscore2=sum(list(hscore_log2.values()))/len(list(hscore_log2.values()))
print('mean hscore for af models with more than 0.1 z score'+str(mean_hscore2))



cnt=0
for x, y in final_ros.items():
    if float(y)==0.1:
        if float(af_dali[x])!=0.1:
            cnt+=1
print('trros w/ z score 0.1 but AF does get score ' + str(cnt))

cnt=0
for x, y in af_dali.items():
    if float(y)==0.1:
        if float(final_ros[x])!=0.1:
            cnt+=1
print('AF w/ z score 0.1 but trRos does get score ' + str(cnt))


######matplotlib 2
ros=((list(final_ros.values())))
ros=[float(x) for x in ros]
AF=((list(af_dali.values())))
AF=[float(x) for x in AF]


df2['pfam']=pfams
df2['ros'] = ros
df2['AF']=AF

#print(df2)

import matplotlib.pyplot as plt
df2.plot(x="pfam", y=["ros", "AF"], kind="bar")
plt.savefig('z_comparison.png')

##########bokeh 2
from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.transform import dodge





df3 = pd.DataFrame(columns=['ros', 'AF'], index=pfams)
df3['ros'] = ros
df3['AF']=AF

ros_mean=(sum(AF))/len(ros)
print(ros_mean)

df3 = df3.reset_index().rename(columns={'index':'qrange'})
data = df3.to_dict(orient='list')
idx = df3['qrange'].tolist()

source = ColumnDataSource(data=data)

p2 = figure(x_range=idx, y_range=(0, df3[['ros','AF']].values.max() + 5),
           plot_height=250, title="Dali Z score comparison of trRos & AF w/pdb TM Pfam struct",
           toolbar_location=None, tools="")

p2.vbar(x=dodge('qrange', -0.3, range=p2.x_range), top='ros', width=0.2, source=source,
       color="blue", legend=False)

p2.vbar(x=dodge('qrange',  -0.1,  range=p2.x_range), top='AF', width=0.2, source=source,
       color="red", legend=False)



p2.x_range.range_padding = 0.02
p2.xgrid.grid_line_color = None
p2.legend.location = 'top_right'
p2.legend.orientation = "horizontal"

#save(p2)




###################distribution graph

#af_dali

ros_dist={'0-5':0,'5-10':0,'10-15':0, '15-20':0,'20-25':0, '25-30':0, '30-35':0,'35-40':0,'40-45':0, '45-50':0,'50-55':0, '55-60':0,'60-65':0,'65-70':0}
cnt=0
cnt_zero=0
for w,x in final_ros.items():
    if float(x) !=0.1:
        for y,z in ros_dist.items(): 
            a,b=y.split('-')
            if float(x)>=float(a) and float(x)<float(b):
                z+=1
                ros_dist[y]=z
                cnt+=1
    else:
        cnt_zero+=1



print(ros_dist)
total_ros=sum(list(ros_dist.values()))
print(total_ros)
print(cnt)
print(len(final_ros))
print(cnt_zero)

af_dist={'0-5':0,'5-10':0,'10-15':0, '15-20':0,'20-25':0, '25-30':0, '30-35':0,'35-40':0,'40-45':0, '45-50':0,'50-55':0, '55-60':0,'60-65':0,'65-70':0}
cnt=0


cnt_zero=0
for w,x in af_dali.items():
    if float(x) !=0.1:
        for y,z in af_dist.items():
            a,b=y.split('-')
            if float(x)>=float(a) and float(x)<float(b):
                z+=1
                af_dist[y]=z
                cnt+=1
    else:
        cnt_zero+=1




print(af_dist)
total_af=sum(list(af_dist.values()))
print(total_af)
print(cnt)
print(len(af_dali))
print(cnt_zero)

bins=(list(ros_dist.keys()))
y1=(list(ros_dist.values()))
y2=(list(af_dist.values()))

p3 = figure(x_range=bins, height=250,
           toolbar_location=None, tools="")
#p3.line(x=bins, y=(list(ros_dist.values())), color="blue", line_width=2)
#p3.line(x=bins, y=(list(af_dist.values())), color="red", line_width=2)
p3.multi_line([bins, bins], [y1, y2], color=['blue', 'red'], alpha=[0.54, 0.40], line_width=3)

save(p3)
