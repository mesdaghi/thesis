f1 = open('../ma_full_results_sorted.txt', "r")
f2 = open('./ma_full_results_sorted.txt', "r")

data = f1.readlines()
keep = len(data) - 50
del data[0:keep]

data2= f2.readlines()
keep2 = len(data2) - 50
del data2[0:keep2]

data3 = []

for i in data:
    for j in data2:
        if i[0:5] == j[0:5]:
            #print(i)
            data3.append(j)

cnt=0
for x in data3:
    cnt += 1
    x = x.strip()
    print(str(cnt) + x)

print(len(data3))

