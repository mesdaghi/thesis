import pandas as pd
import re

#####################################df fro reenterent loops
re_loops = []
with open('/media/shah/sdc/data/re_loops/for_shah.txt') as file:
    for line in file:
        line = line.split('\t')
        re_loops.append(line)

data = pd.DataFrame(re_loops,columns=['pdb_code','title', 'tags'])

re_loops_list = data['pdb_code'].tolist()

####################################list pdbtm_nr
pdbtm_nr=[]
with open('/media/shah/sdc/data/re_loops/pdbtm_nr_list.txt') as file:
    for line in file:
        line = line.strip('\n')
        try:
            a,b = line.split('_')
            a=a.upper()
            pdbtm_nr.append(a)
        except:
            continue

################################list reenterent_nr
re_loops_nr=[]
for x in re_loops_list:
    for y in pdbtm_nr:
        if x==y:
            re_loops_nr.append(y)


#pd.set_option('display.max_colwidth', -1)


########################################################collect all pdbtm alpha xml
#pdb_xml = []
with open('/media/shah/sdc/data/re_loops/pdbtmalpha') as file:
    xml = file.read().split('</pdbtm>')

#print(xml)
#print(len(xml))
#print(len(pdbtm_nr))

################################filter list so only nr reenterent loops present
reenterent_xml = []

for x in re_loops_nr:
    for y in xml:
        code = re.search(x.lower(), y)
        if (code):
            reenterent_xml.append(y)


# print(len(reenterent_xml))
# for x in reenterent_xml:
#     print(x[5:200])

###################################for each reenterent extract pdb_code, chain & seq
reg1 = '<pdbtm xmlns'
reg2 = 'TYPE="alpha"'
reg3 = 'type="L"'
#reg4 = '<'

cnt = 0
extracted_xml_data_chain=[]
pdb_data=[]
for x in reenterent_xml:
    pdb_xml = []

    #print(x)

    seq_list = x.split('CHAIN CHAINID=')
    del seq_list[0]

    #print(seq_list[0:2])

    seq_list_2 = {}
    for sequence in seq_list:
        try:
            a, b, c = sequence.split('SEQ>')
            a = a[1].replace('\n', '')
            b = b.strip('</')
            b = b.strip('>')
            b = b.replace(' ', '')
            seq_list_2[a] = b.replace('\n', '')
        except:
            continue
            #print(sequence + '???????????????????????????')

    #print(seq_list_2)

    #print(x)
    temp = x.split('\n')
    for y in temp:
        #print(y)


        match=re.search(reg1, y)
        if match:
            a,b=y.split('ID=')
        match2 = re.search(reg2, y)
        if match2:
            c,d=y.split('CHAINID=')

            # temp_seq = []
            # match_stop = re.search('</SEQ>', y)
            # cnt+=1




            # # for r in temp:
            # #     match2a = re.search(reg2a, r)
            # #     #index = [ i for i, word in enumerate(temp) if match2a ]
            # #     #print(index)
            # #     #print(match2a)
            #
            # for q in temp:
            #
            #     if match_stop:
            #         break
            #     else:
            #         #print(q)
            #         temp_seq.append(q)
            #
            # temp_seq2=[]
            # for z in temp_seq:
            #     match4 = re.search(reg4, z)
            #     if match4:
            #         continue
            #     else:
            #         temp_seq2.append(z.strip(' '))
            #         print(len(temp_seq2))
            #     new_seq=''.join(temp_seq2)
            #     new_seq = new_seq.replace(' ','')
            #
            #
            # try:
            #     m,new_seq = new_seq.split(')')
            #     new_seq = new_seq[1:]
            # except:
            #     #print(b[1:5] + '_' + d[1] + '\n' + new_seq)
            #     continue

                #print(new_seq)

        match3 = re.search(reg3, y)
        if (match3):
            g,h,i,j,k,l = y.split('=')
            h = re.sub('[^0-9]', '', h) #seq_begins
            j = re.sub('[^0-9]', '', j) #seq_ends
            i = re.sub('[^0-9]', '', i) #pdb_begins
            k = re.sub('[^0-9]', '', k) #pdb_ends

            new_seq = seq_list_2[d[1]]
            new_seq = new_seq[int(h)-1:int(j)]


            extracted_xml_data_chain.append(b[1:5] + ':' + d[1] + ':' + str(h) + ':' + str(j) + ':' + new_seq) #using seq end/begins


            pdb_data.append(b[1:5] + ':' + d[1] + ':' + str(i) + ':' + str(k) + ':' + new_seq) #using pdb ends begins

# for x in extracted_xml_data_chain:
#       print(x)

############################filter each seq leaving only renterent seq
reent_dic = {}
chain_list = []
for x in extracted_xml_data_chain:
    a,b,c,d,e = x.split(':')
    #e = e[int(c)-1:int(d)]
    reent_dic[a + ':' + b + ':' + c + ':' + d] = e
    chain_list.append(a+b)

chain_list = list(dict.fromkeys(chain_list))
#print(len(chain_list))



result = {}
for key, value in reent_dic.items():
     if value not in result.values():
         result[key] = value

final_result = {}
for key, value in result.items():
     if len(value) >=18:
         final_result[key] = value

del final_result['4uwa:A:4187:4204']
del final_result['4dxw:C:166:190']
del final_result['5l25:B:552:577']
del final_result['5mke:D:626:644']


with open('/media/shah/sdc/data/re_loops/final_result.txt', "w") as f:
    for (key, value) in final_result.items():
        f.write('>' + key + '\n')
        f.write(value + '\n')


############################list reenterent_nr with full details
final_pdb_list = []
for key in final_result:
    final_pdb_list.append(key[0:4].upper())

reent_list=[]
with open('/media/shah/sdc/data/re_loops/for_shah.txt') as file:
    for line in file:
        line = line.strip('\n')
        reent_list.append(line)

reent_list_nr_details=[]
for x in final_pdb_list:
    for y in reent_list:
        if x==y[0:4]:
            reent_list_nr_details.append(y)

reent_list_nr_details = list(dict.fromkeys(reent_list_nr_details))


for x in reent_list_nr_details:
     print(x)

print(final_result)
print(len(final_result))


############################################get reent pdb
# filtered_pdb_data=[]
#
# for x in pdb_data:
#     for key, value in final_result.items():
#         if x[0:6]==key[0:6]:
#             filtered_pdb_data.append(x)

#filtered_pdb_data = list(dict.fromkeys(filtered_pdb_data))

pdb_reent_dic = {}
pdb_chain_list = []
for x in pdb_data:
    a,b,c,d,e = x.split(':')
    #e = e[int(c)-1:int(d)]
    pdb_reent_dic[a + ':' + b + ':' + c + ':' + d] = e
    pdb_chain_list.append(a+b)

pdb_chain_list = list(dict.fromkeys(pdb_chain_list))
#print(len(chain_list))

pdb_result = {}
for key, value in pdb_reent_dic.items():
     if value not in pdb_result.values():
         pdb_result[key] = value

pdb_final_result = {}
for key, value in pdb_result.items():
     if len(value) >=18:
         pdb_final_result[key] = value

del pdb_final_result['4uwa:A:4885:4902']
del pdb_final_result['4dxw:C:166:190']
del pdb_final_result['5l25:B:551:576']
del pdb_final_result['5mke:D:626:644']

pdb_list =[]

for key in pdb_final_result.keys():
    pdb_list.append(key)

print(pdb_list)
print(len(pdb_list))


#######create reent pdb files
cnt=0
for x in pdb_list:
    a,b,c,d = x.split(':')
    pdb_code = '/media/shah/sdb/db/pdbtm_chain_split/' + a + '_' + b + '.pdb'
    #print(pdb_code)
    window = [i for i in range(int(c),int(d)+1)]
    #print(window)
    reent_pdb_data = []
    try:
        with open(pdb_code) as file:
            for line in file:
                reent_pdb_data.append(line.strip())
    except:
        cnt += 1
        print(x + str(cnt))


    # reent_pdb_data=[]
    # for y in pdb_codes:
    #     with open('/media/shah/sdb/db/pdbtm_chain_split/' + y) as file:
    #         for line in file:
    #             reent_pdb_data.append(line.strip())

    #print(reent_pdb_data)
    coord_data=[]
    for z in reent_pdb_data:
        z.split(' ')
        match = re.search('ATOM', z)
        if (match):
            coord_data.append(z)

    pdb_file = []
    for i in window:
        for res_number in coord_data:
            number = int(res_number[22:29].strip())
            #print(number)
            if i == number:
                pdb_file.append(res_number)




    with open('/media/shah/sdc/data/re_loops/' + x + '.pdb', "w") as f:
        for j in pdb_file:
            f.write(j + '\n')

























