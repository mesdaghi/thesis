import pandas as pd
from bokeh.plotting import figure,show,output_file
from bokeh.models import Range1d, Legend
from bokeh.models.tools import HoverTool
from bokeh.models import ColumnDataSource
import matplotlib.pyplot as plt
import conkit.io
import conkit.plot
import conkit.io.casp
from conkit.core import Contact, ContactMap
from operator import attrgetter
from itertools import islice

##########################variables#######################
ss_path = './ss.ss2'
top_cons_path = "./query.result"
iupred2a_path = './iupred2a.txt'
consurf_path = './consurf.grades'
sequence_file = "./seq.fasta"
sequence_format = "fasta"
contact_file = "./cont.txt"
contact_format = 'nebcon'
save_fig_path = "./"
html_file = "./cmap.html"

###################format ss data#####################
ss =[[]]
with open(ss_path) as file:
    for line in file:
        line = line.split()
        ss.append(line)
del ss[0:3] #!!!!!!!!!!!!!!!!IMPORTANT: this may change depending on psipred txt file format ss[0] or ss[0:3]!!!!!!!!
print(len(ss))
data = pd.DataFrame(ss,columns=['position','aa', 'prediction', '1', '2', '3'])
print(len(data.index))
data_h = data.loc[(data.prediction == 'H')]
xy_h = data_h['position'].tolist()
xy_h_aa_name = data_h['aa'].tolist()
data_c = data.loc[(data.prediction == 'C')]
xy_c = data_c['position'].tolist()
xy_c_aa_name = data_c['aa'].tolist()
data_e = data.loc[(data.prediction == 'E')]
xy_e = data_e['position'].tolist()
xy_e_aa_name = data_e['aa'].tolist()

###################format topcons data#####################
with open(top_cons_path) as file:
    topcons = file.readlines()

topcons_index = topcons.index('TOPCONS predicted topology:\n') ####can change to other predictions from file eg 'OCTOPUS predicted topology:\n'######
membrane_pred = topcons[topcons_index+1]
membrane_pred_list = []
for x in membrane_pred:
    membrane_pred_list.append(x)
print(membrane_pred_list)
print(len(membrane_pred_list))
membrane_pred_list.remove('\n')
data['mem_pred'] = membrane_pred_list
zeros = [0]*len(membrane_pred_list)
data['zeros'] = zeros
data_i = data.loc[(data.mem_pred == 'i')]
xy_i = data_i['position'].tolist()
data_m = data.loc[(data.mem_pred == 'M')]
xy_m = data_m['position'].tolist()
data_o = data.loc[(data.mem_pred == 'o')]
xy_o = data_o['position'].tolist()

#######format disordered prediction#####################
iupred_data = pd.read_csv(iupred2a_path,sep='\t', comment = '#', skip_blank_lines=True, header=None)
disorder = iupred_data[2].tolist()
data['disorder_pred'] = disorder

data_disorder= data.loc[(data.disorder_pred >= 0.5)]
x_d = data_disorder['position'].tolist()
y_d = []
for x in x_d:
    x = int(x) - 5.5   #############################adjust depending on size of prot eg 168 aa -3, 404 aa =7, 236=5
    y_d.append(x)

data_not_disorder= data.loc[(data.disorder_pred < 0.5)]
x_not_dis = data_not_disorder['position'].tolist()
y_not_dis = []
for x in x_not_dis:
    x = int(x) - 5.5    #############################adjust depending on size of prot eg 168 aa -3, 404 aa =7, 236=5
    y_not_dis.append(x)

###############format consurf prediction####################
consurf =[]
with open(consurf_path) as file:
    for line in file:
        line = line.split()
        #print(line)
        try:
            test=line[0]
            if test.isnumeric():
                consurf.append(line)
        except:
            continue

con_score=[]
for x in consurf:
    x=x[3].replace('*','')    #########################################CHECK!!!!!!!!!! consurf struct =4 consurf seq=3, 404 aa =7, 236=5
    x=int(x)
    con_score.append(x)

data['consurf_pred'] = con_score

consurf_values = list(range(1,10))
x_dct = {}

for x in consurf_values:
    conserved_aa = data.loc[(data.consurf_pred == x)]
    x_dct[x] = conserved_aa['position'].tolist()

y_dct = {}

for y in consurf_values:
    conserved_aa = data.loc[(data.consurf_pred == y)]
    y_dct[y] = conserved_aa['position'].tolist()
    y_dct[y]=[int(x) + 7 for x in y_dct[y]]  #########################################CHECK!!!!!!!!!! consurf struct =4 consurf seq=3

#######format contact prediction#####################
seq = conkit.io.read(sequence_file, sequence_format).top
conpred = conkit.io.read(contact_file, contact_format).top

# Assign the sequence register to your contact prediction
conpred.sequence = seq
conpred.set_sequence_register()

# We need to tidy our contact prediction before plotting
conpred.remove_neighbors(inplace=True)
conpred.sort('raw_score', reverse=True, inplace=True)

# Finally, we don't want to plot all contacts but only the top-L,
# so we need to slice the contact cmap
cmap = conpred[:conpred.sequence.seq_len]

##################Then we can plot the cmap#############################
fig = conkit.plot.ContactMapFigure(cmap, legend=True)

colors2 = {'M':'red', 'o':'yellow', 'i':'green'}
plt.scatter(data.position, data.position, s=50, c=data['mem_pred'].apply(lambda x: colors2[x]))

colors = {'H':'orange', 'C':'blue', 'E':'black'}
plt.scatter(data.position, data.position, s=5, c=data['prediction'].apply(lambda x: colors[x]))

######Print mean  confidence for 3l/2 contacts###############
my_map = conkit.io.read(contact_file, contact_format).top_map

#Filter out contacts
filtered_map=ContactMap("my_map_filtered")
for contact in my_map:
    seq_distance=abs(int(contact.res1_seq)-int(contact.res2_seq))
    if (seq_distance > 12): #filters contacts <12 aa apart
        filtered_map.add(contact)

filtered_map = sorted(filtered_map, key=attrgetter('raw_score'), reverse = True) #sorts contact in order of raw_score

seq_len = int((len(membrane_pred_list)))
top_3l_2 = int((seq_len*3)/2)

iterator = islice(filtered_map, top_3l_2)

iterator = sorted(iterator, key=attrgetter('res1_seq'))
contacts = ContactMap("my_map_filtered")
for contact in iterator:
     contacts.add(contact)

confidence = []
for contact in contacts:
    confidence.append(contact.raw_score)

mean_confidence_score = str((sum(confidence)/(len(confidence))))
print('The mean 3l/2 confidence = ' + mean_confidence_score)
############################################################################


#fig.savefig(save_fig_path)


###################bokeh plot of contacts###################################
dfObj = pd.DataFrame(columns=['id', 'res1', 'res1_chain', 'res1_seq', 'res2', 'res2_chain', 'res2_seq', 'raw_score'])

for x in cmap:
    dfObj = dfObj.append({'id':x.id, 'res1':x.res1, 'res1_chain':x.res1_chain, 'res1_seq':x.res1_seq,
                          'res2':x.res2, 'res2_chain':x.res2_chain, 'res2_seq':x.res2_seq, 'raw_score':x.raw_score}, ignore_index=True)

source = ColumnDataSource(dfObj)

output_file(html_file)

p = figure(x_range=Range1d(0, len(dfObj)), y_range=Range1d(0, len(dfObj)),
           tools = ['pan', 'wheel_zoom', 'box_zoom','reset', 'save']
           ,toolbar_location="above",
           plot_height = 575, plot_width = 700)

p1 = p.circle(x='res1_seq', y='res2_seq', size=3, color='black', source=source)
p.add_tools(HoverTool(renderers=[p1], tooltips=[('Contact', '@id'), ('res1', '@res1'),('res2', '@res2'), ('confidence', '@raw_score')]))
p1a = p.circle(x='res2_seq', y='res1_seq',  size=3, color='black', source=source)
p.add_tools(HoverTool(renderers=[p1a], tooltips=[('Contact', '@id'), ('res1', '@res1'),('res2', '@res2'), ('confidence', '@raw_score')]))

###########bokeh plot of mem_pred########################################
x_i = xy_i
y_i = xy_i
x_m = xy_m
y_m = xy_m
x_o = xy_o
y_o = xy_o

p2 = p.circle(x_i, y_i, size=10, color='green')
p3 = p.circle(x_m, y_m, color='red', size=10)
p4 = p.circle(x_o, y_o, color='yellow', size=10)
###########bokeh plot of ss########################################
aa_properites = {'A':'Non-polar, aliphatic residues',
                 'R':'Positively charged (basic amino acids; non-acidic amino acids); Polar; Hydrophilic; pK=12.5',
                 'N':'Polar, non-charged',
                 'D':'Negatively charged (acidic amino acids); Polar; Hydrophilic; pK=3.9',
                 'C': 'Polar, non-charged',
                 'E': 'Negatively charged (acidic amino acids); Polar; Hydrophilic; pK=4.2',
                 'Q':'Polar, non-charged',
                 'G': 'Non-polar, aliphatic residues',
                 'H':'Positively charged (basic amino acids; non-acidic amino acids); Polar; Hydrophilic; pK=6.0',
                 'I':'Non-polar, aliphatic residues',
                 'L':'Non-polar, aliphatic residues',
                 'K': 'Positively charged (basic amino acids; non-acidic amino acids); Polar; Hydrophilic; pK=10.5',
                 'M': 'Polar, non-charged',
                 'F':'Aromatic',
                 'P':'Non-polar, aliphatic residues',
                 'S':'Polar, non-charged',
                 'T': 'Polar, non-charged',
                 'W': 'Aromatic',
                 'Y':'Aromatic',
                 'V':'Aromatic'
}

cnt=0
h_aa_properies=[]
for x in xy_h_aa_name:
    for y in aa_properites:
        if x==y:
            h_aa_properies.append(aa_properites[y])
            cnt+=1

c_aa_properies=[]
for x in xy_c_aa_name:
    for y in aa_properites:
        if x==y:
            c_aa_properies.append(aa_properites[y])

e_aa_properies=[]
for x in xy_e_aa_name:
    for y in aa_properites:
        if x==y:
            e_aa_properies.append(aa_properites[y])

source2 = ColumnDataSource(data=dict(x=xy_h,y=xy_h,aa_name = xy_h_aa_name,aa_properties=h_aa_properies))
source3 = ColumnDataSource(data=dict(x=xy_c,y=xy_c,aa_name = xy_c_aa_name,aa_properties=c_aa_properies))
source4 = ColumnDataSource(data=dict(x=xy_e,y=xy_e,aa_name = xy_e_aa_name,aa_properties=e_aa_properies))

p5 = p.circle(x='x', y='y', size=3, color='orange',source=source2)
p.add_tools(HoverTool(renderers=[p5], tooltips=[('Position', '@x'), ('Residue Name', '@aa_name'), ('Properties', '@aa_properties')]))
p6 = p.circle(x='x', y='y', color='blue', size=3,source=source3)
p.add_tools(HoverTool(renderers=[p6], tooltips=[('Position', '@x'), ('Residue Name', '@aa_name'), ('Properties', '@aa_properties')]))
p7 = p.circle(x='x', y='y', color='pink', size=3,source=source4)
p.add_tools(HoverTool(renderers=[p7], tooltips=[('Position', '@x'), ('Residue Name', '@aa_name'), ('Properties', '@aa_properties')]))

###########bokeh plot of disorder########################################

x_d = x_d
y_d = y_d
x_nd = x_not_dis
y_nd = y_not_dis

p8 = p.circle(x_d, y_d, size=5, color='lime')
p9 = p.circle(x_nd, y_nd, color='grey', size=5)

############bokeh plot of conservation##############################

Blues = {1:'#f7fbff',2:'#deebf7',3:'#c6dbef',4:'#9ecae1',5:'#6baed6',6:'#4292c6',7:'#2171b5',8:'#08519c',9:'#08306b'}

for x in Blues:
    p.triangle(x_dct[x], y_dct[x], size=5, color=Blues[x])

####################################################################
legend = Legend(items=[
    ("Contact"   , [p1]),
    ("Mem_pred-I" , [p2]), ("Mem_pred-M" , [p3]),  ("Mem_pred-O" , [p4]),
    ("SS-H" , [p5]), ("SS-C" , [p6]), ("SS-E" , [p7]),
    ("Disorder" , [p8]), ("Ordered" , [p9])
], location="center")

p.add_layout(legend, 'right')
show(p)

######################################################################
