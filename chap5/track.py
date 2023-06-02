from os import walk


f = []
f_dic = {}
for (dirpath, dirnames, filenames) in walk('./'):
    f.extend(filenames)
    break

fasta=[]
for x in f:
    if x[-6:] == '.fasta':
        y='./'+x
        fasta.append(y)

track={}

for x in fasta:
    with open(x, "r") as file:
        first_line = file.readline()
        a,b,c=first_line.split('_')
        a=a.strip('>')
        track[a]=b

print(track)

f = open("./track.txt", "w")
for a,b in track.items():
    f.write(a+'_'+b+'\n')
f.close()
