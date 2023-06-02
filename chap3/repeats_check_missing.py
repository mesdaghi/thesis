import subprocess
from os import walk
import os

f = []
for (dirpath, dirnames, filenames) in walk('./sequences'):
    f.extend(filenames)
    break

print(f)

f2 = []
for (dirpath, dirnames, filenames) in walk('./final_models'):
    f2.extend(filenames)
    break

print(f2)

for x in f:
    for y in f2:
        if x[0:7]==y[0:7]:
            print(x)
            try:
                f.remove(x)
            except:
                continue


for x in f:
    for y in f2:
        if x[0:7]==y[0:7]:
            print(x)
            try:
                f.remove(x)
            except:
                continue

for x in f:
    for y in f2:
        if x[0:7]==y[0:7]:
            print(x)
            try:
                f.remove(x)
            except:
                continue
for x in f:
    for y in f2:
        if x[0:7]==y[0:7]:
            print(x)
            try:
                f.remove(x)
            except:
                continue


print(f)
print(len(f))

f3 = []
for (dirpath, dirnames, filenames) in walk('/media/shah/sdc/data/dan/sequences'):
    f3.extend(filenames)
    break

print(f3)


for x in f:
    for y in f3:
        if x==y:
            print(x)
            f.remove(x)

for x in f:
    for y in f3:
        if x==y:
            print(x)
            f.remove(x)

print(f)
print(len(f))
