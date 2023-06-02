from os import walk

f=[]
for (dirpath, dirnames, filenames) in walk('/media/shah/sdc/data/pfam_reloop_screen/all_v_all/seq/'):
    f.extend(filenames)
    break

for x in f:
    fasta =[]
    with open("/media/shah/sdc/data/pfam_reloop_screen/all_v_all/seq/"+x) as file:
    
        for line in file:
            fasta.append(line.strip())

        fasta_len = len(fasta)
        fasta[1:fasta_len] = [''.join(fasta[1:fasta_len])]

        fasta_file = open("/media/shah/sdc/data/pfam_reloop_screen/all_v_all/seq2/"+x, "w")
        whole_seq = fasta[1]
        len_seq = len(whole_seq)
        print(len(whole_seq))
        a,b=x.split('.')
        fasta_file.write('>' +a+ '\n' + whole_seq)


