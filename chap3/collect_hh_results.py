import os
import pandas as pd

re_ent_lst=[]
raw_data = []
hh_data = {}

for root, dirs, files in os.walk("/media/shah/sdc/data/re_loops/hh/results/ss/"):
    for file in files:
        if file.endswith(".hhr"):

            f = open(os.path.join("/media/shah/sdc/data/re_loops/hh/results/ss/", file), "r")
            lines = f.readlines()

            a,query = lines[0].split('         ')
            re_ent_lst.append(query.strip())

            tmp = []
            for line in lines:
                new_line = line.strip('  ')
                if new_line[0].isnumeric():
                    tmp.append(new_line)

            query_data = []

            for x in tmp:
                hit_data = {}
                x = x.replace('  ', ' ')
                x = x.replace('   ', ' ')
                x = x.replace('    ', ' ')
                x = x.replace('     ', ' ')
                x = x.replace('      ', ' ')
                x = x.replace('       ', ' ')
                x = x.replace('  ', ' ')
                x = x.replace('  ', ' ')

                try:
                    a,b,c,d,e,f,g,h,i,j,k= x.split(' ')
                except:
                    print(x)
                    exit()
                raw_data = [c, d, e, f]
                item = b
                hit_data[item] = raw_data
                query_data.append(hit_data)

            hh_data[query] = query_data

row_names = []
for key in hh_data:
    key = key.strip()
    row_names.append(key)

df_prob = pd.DataFrame(index=row_names, columns=re_ent_lst)
df_e = pd.DataFrame(index=row_names, columns=re_ent_lst)
df_p = pd.DataFrame(index=row_names, columns=re_ent_lst)
df_score = pd.DataFrame(index=row_names, columns=re_ent_lst)

cnt_query = 0
cnt_hit = 0

for key, value in hh_data.items():
    cnt_query += 1
    key = key.strip()
    for x in value:
        cnt_hit +=1
        for a, b in x.items():
            b = b[0]
            #print(str(cnt_query) + ' ' + key + ' ' + 'X' + ' ' +str(cnt_hit)+ ' ' +  a + ' ' +b)
            df_prob.at[key, a] = b

print(df_prob)


with open('/media/shah/sdc/data/re_loops/hh/results/ss/clans_sim_matix.txt', "w") as f:   ##########change
    f.write('sequences=' + str(len(df_prob)) + '\n' + '<seqs>' + '\n')    ##########################change
    for x in list(df_prob.columns.values):      #############################change
        f.write('>' + x + '\n')
    f.write('</seqs>\n<mtx>\n')

    Row_list = []
    for i in range((df_prob.shape[0])):         #############################change
        Row_list.append(list(df_prob.iloc[i, :]))       #############################change

    for x in Row_list:
        for y in x:
            if str(y).replace('.', '', 1).isdigit():
                f.write(str(y) + ' ')
            else:
                f.write('0' + ' ')
        f.write('\n')
    f.write('</mtx>')
