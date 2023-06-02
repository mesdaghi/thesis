import csv

filename = "./log.txt"
file = open(filename, "r")
data = []

for line in file:
    words = line.split()
    if words[0] == 'T':
        my_pdbID_code = words[1]
        my_pdbID_code = my_pdbID_code[0:4]
        my_pdbID = "/media/shah/sdb/db/pdbtm/" + my_pdbID_code + '.pdb'
        fp = open(my_pdbID)
        lines = fp.readlines()
        title = lines[1]
        title = title[10:80]
        words.append(title)
        fp.close()
        data.append(words)

for x in data:
    print(*x)

data = []
cnt = 0
cnt2 = 0

filename = "./log.txt"
file = open(filename, "r")
for line in file:
    words = line.split()
    if words[0] == 'M' and words[3] == '1.000':
        score = words[3]
        data.append(score)
    if words[0] == 'M' or words[0] == 'S':
        cnt += 1
    if words[0] == 'M':
        cnt2 += 1




number_hits = len(data)
percent = (number_hits/cnt)*100
percent2 = (number_hits/cnt2)*100
print('Full count = ' + str(cnt))
print('No pdbs with score of 1 = ' + str(len(data)))
print('Percentage out of full count = ' + str(percent))
print('Count excluding skipped structures = ' + str(cnt2))
print('Percentage excluding skipped structures = '+ str(percent2))

f = open("./ma_results_formatted.txt", "w")
f2 = open("./ma_results_formatted.txt", "a")
with f:
    wr = csv.writer(f, quoting=csv.QUOTE_ALL)
    wr.writerows(data)
    f.close()

with f2:
    f2.write('Full count = ' + str(cnt))
    f2.write('No pdbs with score of 1 = ' + str(len(data)) + '\n')
    f2.write('Percentage out of full count = ' + str(percent) + '\n')
    f2.write('Count excluding skipped structures = ' + str(cnt2) + '\n')
    f2.write('Percentage excluding skipped structures = ' + str(percent2) + '\n')

