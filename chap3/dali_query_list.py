import re
paths =[]
with open("/Users/shahrammesdaghi/Downloads/log.txt") as file:
    for line in file:
        line = [line.rstrip()]
        #print(line)
        path = line[0]
        x = re.search('centroid', path)
        if (x):
            paths.append(path)
            #print(paths)

f = open("/Users/shahrammesdaghi/Downloads/query.list", "w")
for x in paths:
    f.write(x[21:] + '\n')