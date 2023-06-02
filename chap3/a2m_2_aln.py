import re

with open('3org.a2m') as myFile:
  text = myFile.read()
result = text.split('>')

data=[]

for i in result:
    homolog = i.split('\n')
    data.append(homolog)

data = [x for x in data if x != ['']]

cnt = 0
f = open("3org.aln", "w")
for i in data:
    i = list(filter(None, i))
    del i[0]
    i = ''.join(i)
    remove_lower = lambda text: re.sub('[a-z]', '', text)
    i = remove_lower(i)
    cnt += 1
    print(i)
    f.write(i+'\n')
print(cnt)


