import re

track={}

with open('./track_dali_all.txt', "r") as file:
    lines = file.readlines()
    for x in lines:
        a=x[0:4]
        b=(x[5:]).strip()
        #a,b=x.split('_')
        #b=b.strip('\n')
        track[a]=b
#pfam = track[z[1][0:4]]
print(track)

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

print(clans_data)

with open('./clans_sim_matix_values_w_pfamClans.txt', "w") as f:
    f.write('sequences=' + matrix_data[0][0] + '<seqs>' + '\n')
    for x in matrix_data[1:]:
        #f.write('>' + x[0] + '\n')
        pfam=track[x[0][0:4]]
        if pfam in clans_data.keys():
            f.write('>' + pfam +'#'+clans_data[pfam]+ '\n')
        else:
            f.write('>' + pfam +'#'+'NONE'+ '\n')
    f.write('</seqs>\n<mtx>\n')

    for x in matrix_data[1:]:
        for y in x[1:]:
            match = re.search('\n', y)
            if match:
                y = y.strip()
                #y = 1/(float(y))
                y = (float(y))
                f.write(str(y) + '\n')
                #f.write(str(y) + '\n')
            else:
                y = y.strip()
                #y = 1/float(y)
                y = float(y)
                f.write(str(y) + ' ')

    f.write('</mtx>')




