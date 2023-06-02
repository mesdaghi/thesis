import os

path = '/media/shah/sdb/db/pdbtm_chain_split'

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.pdb' in file:
            files.append(os.path.join(r, file))

file = open('/home/shah/progs/map_align/pdbtm_redun_list.txt', 'w')
cnt = 0
for f in files:
    cnt += 1
    path = f[36:42]
    print(f + ' ' + f[37:43])
    file.write(f + ' ' + f[37:43] + '\n')
print(cnt)
