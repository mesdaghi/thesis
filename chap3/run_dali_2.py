from os import walk
import subprocess
import os
import shutil

f = []
for (dirpath, dirnames, filenames) in walk('./sequences'):
    f.extend(filenames)
    break

#os.mkdir('./final_models')

#for x in f:
    #print(x)
    #f2 =[]
    #for (dirpath, dirnames, filenames) in walk('./'+x[0:7]+'/'+x[0:7]+'_models'):
        #f2.extend(filenames)
        #break
    #print(f2)
    #for y in f2:
        #print(y[0:5])
        #print(y[-3:])
        #if y[0:5] == 'final' and y[-3:] == 'pdb':   
            #print(x)
            #print(y)
            #shutil.copy('./'+ x[0:7]+ '/'+ x[0:7] + '_models/'+ y ,'./final_models/')
            #os.rename('./final_models/' + y , './final_models/' + x[0:7] + '_' + y[-5] + '.pdb')

f3 = []
for (dirpath, dirnames, filenames) in walk('./final_models'):
    f3.extend(filenames)
    break

#file = open('./final_models' + '/dali' + '/query.list', "w")
#for x in f3:
 #   print(x[-9:-6]+x[-5]+'A'+'\n')
  #  file.write(x[-9:-6]+x[-5]+'A'+'\n')
    #if os.path.exists("dali.lock"):
        #os.remove("dali.lock")
   # cmd1 = 'perl -I bin /home/shah/progs/DaliLite.v4/bin/import.pl' + ' ' + './final_models/'   + x + ' ' + x[-9:-6]+x[-5] + ' ' + './final_models/dali/DAT'
    #print(cmd1)
    #subprocess.call(cmd1, cwd = ('./') , shell=True)


cmd2 = 'perl -I bin /home/shah/progs/DaliLite.v4/bin/dali.pl --query ' + '/media/shah/sdc/data/new/final_models/dali/query.list ' + '--db ' + '/home/shah/progs/DaliLite.v4/target.list ' + '--dat1 ' + '/media/shah/sdc/data/new/final_models/dali/DAT' + ' --dat2 '  + '/home/shah/progs/DaliLite.v4/DAT_pdb'
print(cmd2)
subprocess.call(cmd2, cwd = ('./final_models/dali') , shell=True)



