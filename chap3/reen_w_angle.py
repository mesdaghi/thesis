# dict_data = {}
# with open('/media/shah/sdc/data/re_loops/final_result.txt') as f:
#     for key in f:
#         dict_data[key.strip()] = next(f).strip()

# with open('/media/shah/sdc/data/re_loops/interhlx.txt', 'w') as f2:
#     for key, value in dict_data.items():
#         len_seq = int(len(value))
#         f2.write(key[1:len_seq]+ '.pdb' + ' ' + '1' + ' ' + '6' + ' ' + str(len_seq-6) + ' ' + str(len_seq) +  '\n')

import re
# from os import listdir
# from os.path import isfile, join
#
# path = '/media/shah/sdc/data/re_loops/pdb_files/'
# pdb_files = [f for f in listdir(path) if isfile(join(path, f))]
#
# with open('/media/shah/sdc/data/re_loops/interhlx.txt', 'w') as f2:
#     for x in pdb_files:
#         a,b,c,d = x.split(':')
#         start = int(c)
#         end, e = d.split('.')
#         end = int(end)
#         #seq_len = end - start
#         hel1_start = start
#         hel1_end = start + 8
#         hel2_start = end - 8
#         hel2_end = end
#         f2.write(path + x + ' ' + str(hel1_start) + ' ' + str(hel1_end) + ' ' + str(hel2_start) + ' ' + str(hel2_end) + '\n')

angles_file = '/media/shah/sdc/data/re_loops/pdb_files/output_file'

dict_data = {}

f = open(angles_file, 'r')
lines = f.readlines()

stripped_lines = []
for x in lines:
    x = x.strip('\n')
    if x != '':
        stripped_lines.append(x)

stripped_lines = stripped_lines[:len(stripped_lines)-4]
stripped_lines = dict(zip(stripped_lines[::2], stripped_lines[1::2]))

angle_data = []

for key, value in stripped_lines.items():
    a,b = key.split('.')
    c,d,e,f,g,h,i, pdb_code = a.split('/')
    j, angle, k =  value.split('e')
    angle, l = angle.split('D')
    #angle = angle.strip(' -')
    angle = angle.strip()
    angle = float(angle)
    angle = 180 - angle
    angle = round(angle,2)
    angle_data.append(pdb_code + ':' + str(angle) + 'DEG')

for x in angle_data:
    print(x)





