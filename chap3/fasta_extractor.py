
fasta_file = '/media/shah/sdc/data/w9dy28/w9dy28.fasta'
extract_from = 1
extract_to = 84
path_new_fasta = '/media/shah/sdc/data/w9dy28/hhalign/'
prot_name = 'w9dy28'

fasta =[]
with open(fasta_file) as file:
    for line in file:
        fasta.append(line.strip())

fasta_len = len(fasta)
fasta[1:fasta_len] = [''.join(fasta[1:fasta_len])]

f = open(path_new_fasta + prot_name + '_' + str(extract_from) + '_' + str(extract_to) + '.fasta', "w")
whole_seq = fasta[1]
len_seq = len(whole_seq)
print(len(whole_seq))

selection = whole_seq[extract_from-1:extract_to]
print(selection)
print(len(selection))
f.write(fasta[0] + '\n' + selection)

