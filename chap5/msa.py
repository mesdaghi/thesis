seq_file = './code_pfam_seqac_seq_list.txt'
with open(seq_file) as file:
    for line in file:
        a,b,c,d = line.split('_')
        fasta_file =open( './' + a + '.fasta', 'w')
        fasta_file.write('>' + a + '_' + b + '_' + c + '\n' + d)
        fasta_file.close()
