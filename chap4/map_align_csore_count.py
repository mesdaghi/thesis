filename = "/Users/shahrammesdaghi/Downloads/vmp1_nr_log.txt"
file = open(filename, "r")
data = []
cnt = 0
cnt2 = 0

for line in file:
    words = line.split()
    if words[0] == 'M' and words[3] == '1.000':
        score = words[3]
        data.append(score)
    if words[0] == 'M' or words[0] == 'S':
        cnt += 1
    if words[0] == 'M':
        cnt2 += 1

number_hits = len(data)
percent = (number_hits/cnt)*100
percent2 = (number_hits/cnt2)*100
print(cnt)
print(len(data))
print(percent)
print(cnt2)
print(percent2)

