import sys
from Bio import SeqIO
from os import walk

f=[]
for (dirpath, dirnames, filenames) in walk('/media/shah/sdc/data/pfam_reloop_screen/all_v_all/pfam_models/'):
    f.extend(filenames)
    break

cnt=0
for x in f:
    a,b=x.split('.')
    PDBFile = '/media/shah/sdc/data/pfam_reloop_screen/all_v_all/pfam_models/'+x
    
    with open(PDBFile, 'r') as pdb_file:
        try:
            for record in SeqIO.parse(pdb_file, 'pdb-atom'):
                print('>' + a)
                print(record.seq)
            #f = open("./seq/" +a+'.fasta', "w")
            #f.write('>' + a + '\n')
            #f.write(record.seq)
            #f.close()
                SeqIO.write(record, './seq/'+a+".fasta", "fasta")
        except:
            cnt+=1

print(cnt)
