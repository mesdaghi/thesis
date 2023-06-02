import re

matrix_data= []
with open('/media/shah/sdc/data/f1000/dali2/ordered') as file:
    for line in file:
        line = line.split('\t')
        matrix_data.append(line)

with open('/media/shah/sdc/data/f1000/dali2/clans_sim_matix_values.txt', "w") as f:
    f.write('sequences=' + matrix_data[0][0] + '<seqs>' + '\n')
    for x in matrix_data[1:]:
        f.write('>' + x[0] + '\n')
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




