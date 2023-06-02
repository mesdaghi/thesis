from fpdf import FPDF
import subprocess
from os import walk
import os
import pandas as pd

f = []
for (dirpath, dirnames, filenames) in walk('./sequences'):
    f.extend(filenames)
    break

print(f)
print(len(f))

row_names = []
col_names = ['uniprot', 'meta_5', 'meta_1']

for x in f:
    row_names.append(x[0:7])

df_neff = pd.DataFrame(index=row_names, columns=col_names)

################add unitprot to neff df
uniprot_file = open('/media/shah/sdc/data/dan/neff.txt','r')
content = uniprot_file.readlines()
neff_dic={}

for x in content:
    a,b = x.split(' ')
    neff_dic[a] = b

for key, value in neff_dic.items():
    df_neff.at[key, 'uniprot'] = int(value.strip())

###############add meta 1 iter to neff df
uniprot_file = open('/media/shah/sdc/data/new/neff.txt','r')
content = uniprot_file.readlines()
neff_dic={}

for x in content:
    a,b = x.split(' ')
    neff_dic[a] = b

for key, value in neff_dic.items():
    df_neff.at[key, 'meta_1'] = int(value.strip())


##############add meta 5 iter to neff df

uniprot_file = open('/media/shah/sdc/data/djr/neff.txt','r')
content = uniprot_file.readlines()
neff_dic={}

for x in content:
    a,b = x.split(' ')
    neff_dic[a] = b

for key, value in neff_dic.items():
    df_neff.at[key, 'meta_5'] = int(value.strip())

######################print pdf

print(df_neff)

w = 70
h = 70
pdf = FPDF(orientation = 'P')
pdf.add_page()
cnt=0
for x in f:
    cnt+=1
    if cnt==1:
        print(x[0:7])
        image_1='/media/shah/sdc/data/dan/cmaps/'+x[0:7]+'_wo_meta.png'
        pdf.image(image_1, x=30, y=10, w=w, h=h)
        neff_value = df_neff.loc[x[0:7],"uniprot"]
        pdf.set_font("Arial", size=12)
        pdf.text(x= 30, y= 10, txt=x[0:7]+'_uniprot Neff='+str(neff_value))
        #pdf.text(x= 100, y= 10, txt=x[0:7]+'_w_meta' )
        try:
            image_2='./cmaps/'+x[0:7]+'_w_meta_5_iter.png'
            pdf.image(image_2, x=120, y=10, w=w, h=h)
            neff_value = df_neff.loc[x[0:7],"meta_5"]
            pdf.text(x= 100, y= 10, txt=x[0:7]+'_w_meta 5 iter Neff='+str(neff_value) )
        except:
            continue
    elif cnt==2:
        print(x[0:7])
        image_1='/media/shah/sdc/data/dan/cmaps/'+x[0:7]+'_wo_meta.png'
        #image_2='./cmaps/'+x[0:7]+'_w_meta.png'
        pdf.image(image_1, x=30, y=80, w=w, h=h)
        #pdf.image(image_2, x=120, y=80, w=w, h=h)
        neff_value = df_neff.loc[x[0:7],"uniprot"]
        pdf.set_font("Arial", size=12)
        pdf.text(x= 30, y= 80, txt=x[0:7]+'_uniprot Neff='+str(neff_value) )
        #pdf.text(x= 100, y= 80, txt=x[0:7]+'_w_meta' )
        try:
            image_2='./cmaps/'+x[0:7]+'_w_meta_5_iter.png'
            pdf.image(image_2, x=120, y=80, w=w, h=h)
            neff_value = df_neff.loc[x[0:7],"meta_5"]
            pdf.text(x= 100, y= 80, txt=x[0:7]+'_w_meta 5 iter Neff='+str(neff_value) )
        except:
            continue
    elif cnt==3:
        print(x[0:7])
        image_1='/media/shah/sdc/data/dan/cmaps/'+x[0:7]+'_wo_meta.png'
        #image_2='./cmaps/'+x[0:7]+'_w_meta.png'
        pdf.image(image_1, x=30, y=150, w=w, h=h)
        #pdf.image(image_2, x=120, y=150, w=w, h=h)
        neff_value = df_neff.loc[x[0:7],"uniprot"]
        pdf.set_font("Arial", size=12)
        pdf.text(x= 30, y= 150, txt=x[0:7]+'_uniprot Neff='+str(neff_value) )
        #pdf.text(x= 100, y= 150, txt=x[0:7]+'_w_meta' )
        try:
            image_2='./cmaps/'+x[0:7]+'_w_meta_5_iter.png'
            pdf.image(image_2, x=120, y=150, w=w, h=h)
            neff_value = df_neff.loc[x[0:7],"meta_5"]
            pdf.text(x= 100, y= 150, txt=x[0:7]+'_w_meta 5 iter Neff='+str(neff_value) )
        except:
            continue
    elif cnt==4:
        print(x[0:7])
        cnt=0
        image_1='/media/shah/sdc/data/dan/cmaps/'+x[0:7]+'_wo_meta.png'
        #image_2='./cmaps/'+x[0:7]+'_w_meta.png'
        pdf.image(image_1, x=30, y=220, w=w, h=h)
        #pdf.image(image_2, x=120, y=220, w=w, h=h)
        neff_value = df_neff.loc[x[0:7],"uniprot"]
        pdf.set_font("Arial", size=12)
        pdf.text(x= 30, y= 220, txt=x[0:7]+'_uniprot Neff='+str(neff_value) )
        #pdf.text(x= 100, y= 220, txt=x[0:7]+'_w_meta' )
        try:
            image_2='./cmaps/'+x[0:7]+'_w_meta_5_iter.png'
            pdf.image(image_2, x=120, y=220, w=w, h=h)
            neff_value = df_neff.loc[x[0:7],"meta_5"]
            pdf.text(x= 100, y= 220, txt=x[0:7]+'_w_meta 5 iter Neff='+str(neff_value) )
            pdf.add_page()
        except:
            pdf.add_page()
            continue

    

pdf.output("repeat_cmaps_5_iter.pdf", "F")
