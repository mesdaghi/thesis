import collections
import csv

filename = "./log.txt"
file = open(filename, "r")

new_data = {}

for line in file:
    words = line.split()
    if words[0] == 'M':
        data = []
        score = float(words[4]) + float(words[5])
        my_pdbID_code = words[1]
        my_pdbID_code = my_pdbID_code[0:4]
        my_pdbID = "/media/shah/sdb/db/pdbtm/" + my_pdbID_code + '.pdb'
        fp = open(my_pdbID)
        lines = fp.readlines()
        title = lines[1]
        title = title[10:80]
        data.append(words[1])
        data.append(str(score))
        data.append(title)
        fp.close()
        new_data[score]=data

sorted_new_data = sorted(new_data.items(), key=lambda kv: kv[0])

sorted_dict = collections.OrderedDict(sorted_new_data)

for x in sorted_dict:
    y = sorted_dict[x]
    print(*y)

f = open("./ma_full_results_sorted_test.txt", "w")
with f:
    for x in sorted_dict:
        y = sorted_dict[x]
        for i in y:
            f.write(i + '\t')
        f.write('\n')
        #wr = csv.writer(f, quoting=csv.QUOTE_ALL)
        #wr.writerows(y)
        #f.close()
