import operator
from os import walk
import shutil

d=[]
for (dirpath, dirnames, filenames) in walk('/media/shah/sdc/data/pfam_reloop_screen/all_v_all/mrparse/'):
    d.extend(dirnames)
    break

for directory in d:
    my_file = open("/media/shah/sdc/data/pfam_reloop_screen/all_v_all/mrparse/"+directory+"/mrparse.log", "r")

#my_file = open("/media/shah/sdc/data/pfam_reloop_screen/all_v_all/mrparse/mrparse_993/mrparse.log", "r")

    content_list = my_file.readlines()
    relevant_lines=[]
    temp_dic={}

    for w,x in enumerate(content_list):
        #print(x)
        if x[0:5]=='Query':
            query=x.split()
            if query[1][0]=='P':
                #print(query[1])
                #pfam,b,c,d=query[1].split('_')
                pfam_line=query[1].split('_')
                pfam=pfam_line[0]
        elif x[0]=='>' and x[3]=='A':
            #a,b,c=x.split('-')
            af_model=x.split('-')

            temp_list=content_list[w+3].split()
            temp_dic[af_model[1]]=float(temp_list[2])
        

    if temp_dic:
        top_model=max(temp_dic.items(), key=operator.itemgetter(1))[0]
        #print(top_model)
        print(pfam+' '+str(temp_dic[top_model]))

    f=[]
    #for (dirpath, dirnames, filenames) in walk('/media/shah/sdc/data/pfam_reloop_screen/all_v_all/mrparse/mrparse_993/models'):
    for (dirpath, dirnames, filenames) in walk('/media/shah/sdc/data/pfam_reloop_screen/all_v_all/mrparse/'+directory+'/models'):
        f.extend(filenames)
        break

    #print(f)

    for x in f:
        if temp_dic:
            a,b,c,d=x.split('-')
            #print(b)
            #print(top_model)
            #if b==top_model:
                #print('vvvvvvvvvvvvvvvvvv')
             #   shutil.copyfile('/media/shah/sdc/data/pfam_reloop_screen/all_v_all/mrparse/'+directory+'/models/'+x,'/media/shah/sdc/data/pfam_reloop_screen/all_v_all/af_models/af_' + pfam + '.pdb')

