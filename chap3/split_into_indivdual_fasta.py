fasta_file = '/media/shah/sdc/data/re_loops/hh/final_result_w_snare.txt'

dict_data = {}

f = open(fasta_file, 'r')
lines = f.readlines()

stripped_lines = []
for x in lines:
    x = x.strip('\n')
    if x != '':
        stripped_lines.append(x)

#stripped_lines = stripped_lines[:len(stripped_lines)-4]
stripped_lines = dict(zip(stripped_lines[::2], stripped_lines[1::2]))
print(stripped_lines)
print(len(stripped_lines))

for key,value in stripped_lines.items():
    file_name = key[1:len(key)]
    file_name = file_name.replace(":", "_")
    with open('/media/shah/sdc/data/re_loops/hh/results/' + file_name + '.fasta', "w") as f:
        f.write(key + '\n' + value)

