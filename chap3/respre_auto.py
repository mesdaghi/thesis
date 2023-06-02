import subprocess
from os import walk
import os
import shutil

f = []
for (dirpath, dirnames, filenames) in walk('./sequences'):
    f.extend(filenames)
    break

#cmd_list=[]

#for x in f:
 #   cmd_list.append('python ~/progs/ResPRE/respre.py'+ ' ./B' + x[1:7] + '.aln ./P' + x[1:7] + '.out')
 #   cmd_list.append('python ~/progs/ResPRE/respre.py'+ ' ./P' + x[1:7] + '.aln ./P' + x[1:7] + '.out &')

#print(len(cmd_list))

#for y in cmd_list[30:]:
 #   directory = './P' + y[-26:-20]
 #   directory = './P' + y[-24:-18]
  #  print(directory)
   # subprocess.call(y, cwd = directory , shell=True)






###########################plot##############

#cmd_list_2=[]

#for x in f:
 #   cmd_list_2.append('/home/shah/progs/conkit/bin/conkit-plot cmap ' + '../sequences/' + x + ' fasta ' + x[0:7] + '.out flib &')

#print(cmd_list_2)

#log=[]
#f = open("contact_log.txt", "w")
#for y in cmd_list_2:
 #   directory = './' + y[-18:-11]
  #  print(directory)
   # respre_file = directory + '/' + directory[2:] + '.out'
    #if os.path.isfile(respre_file):
     #   subprocess.call(y, cwd = directory , shell=True)
    #else:
     #   log.append(directory)

#print(log)
#print(len(log))

#for x in log:
 #   f.write(x + '\n')
#f.write(str(len(log)))
#f.close()


#######################collect maps##########

os.mkdir('./cmaps')

for x in f:
    print(x)
    f2 =[]
    for (dirpath, dirnames, filenames) in walk('./'+x[0:7]+'/'):
        f2.extend(filenames)
        break
        print(f2)
    for y in f2:
        print(y[0:5])
        print(y[-3:])
        if y[-3:] == 'png':
            print(x)
            print(y)
            shutil.copy('./'+ x[0:7]+ '/' + y ,'./cmaps/')
            os.rename('./cmaps/' + y , './cmaps/' + x[0:7] + '_w_meta_5_iter' + '.png')
