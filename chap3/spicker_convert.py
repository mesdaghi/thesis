import os

aa = {'A':'ALA', 'R':'ARG', 'N':'ASN','D':'ASP','B':'ASX', 'C':'CYS','E':'GLU','Q':'GLN', 'Z':'GLX', 'G':'GLY',\
      'H':'HIS', 'I':'ILE', 'L':'LEU', 'K':'LYS', 'M':'MET', 'F':'PHE', 'P':'PRO', 'S':'SER', 'T':'THR', 'W':'TRP'\
      ,'Y':'TYR', 'V':'VAL'}

fasta=[]
cnt = 0

f = open("/home/shah/seq/w9dy28/w9dy28.fasta", "r")
content = f.readlines()
for line in content:
    line = line.rstrip()
    if not line.startswith(">"):
        for x in line:
            fasta.append(x)

#to create seq.dat file
for x in fasta:
    cnt += 1
    print('   ' + str(cnt) + '   ' + aa[x])
    if cnt <= 9:
        seq = open("seq.dat", "a")
        seq.write('    ' + str(cnt) + '   ' + aa[x] + '\n')
    elif cnt > 9 and cnt <= 99:
        seq = open("seq.dat", "a")
        seq.write('   ' + str(cnt) + '   ' + aa[x] + '\n')
    elif cnt >= 100:
        seq = open("seq.dat", "a")
        seq.write('  ' + str(cnt) + '   ' + aa[x] + '\n')

#to create tra.in file
path = open("tra.in", "w")
path.write(' ' + '1000' + ' ' + '1' + ' ' + '1' + '\n')
for root, dirs, files in os.walk(os.path.abspath("/home/shah/seq/w9dy28/rosetta/models/")):
    for file in files:
        path = open("tra.in", "a")
        #print(os.path.join(root, file))
        paths = str((os.path.join(root, file)))
        print(paths)
        path.write(paths + '\n')

#to create the rmsinp file
length = open("rmsinp", "w")
length.write('1' + '  ' + str(cnt) + '\n' + str(cnt))




