import os

path = './'
path_len = len(path)

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.pdb' in file:
            files.append(os.path.join(r, file))

with open('pdb_list.txt', 'w') as file:
    for f in files:
        file.write(f[path_len:] + '\n')
