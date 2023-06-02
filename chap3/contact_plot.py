# Import
import conkit.io, conkit.io.casp
from conkit.core import Contact, ContactMap
from operator import attrgetter
from itertools import islice
import matplotlib.pyplot as plt


#Read map
my_map = conkit.io.read('/media/shah/sdc/data/atg9a/dmp/1_500/atg91_1_500.deepmetapsicov.con', 'nebcon').top_map
print("Before filter: %s" % my_map.ncontacts)

#Filter out contacts
filtered_map=ContactMap("my_map_filtered")
for contact in my_map:
    seq_distance=abs(int(contact.res1_seq)-int(contact.res2_seq))
    if (seq_distance > 12): #filters contacts <12 aa apart
        filtered_map.add(contact)





filtered_map = sorted(filtered_map, key=attrgetter('raw_score'), reverse = True) #sorts contact in order of raw_score


print(filtered_map)

coord = []
for contact in filtered_map:
    if contact.raw_score>0.5:
        coord.append(contact.id)
#print(coord)
x,y = zip(*coord)
plt.xlim(0, 550)
plt.ylim(0, 550)
plt.scatter(x, y, color='black', s=5)
plt.scatter(y, x, color='black', s=5)

plt.show()




# contact_len = len(filtered_map)
#
# for contact in filtered_map[(contact_len-1):contact_len]:
#     seq_len = contact.res2_seq
#
# top_3l_2 = int((seq_len*3)/2)
#
# iterator = islice(filtered_map, top_3l_2)
#
# iterator = sorted(iterator, key=attrgetter('res1_seq'))
# contacts = ContactMap("my_map_filtered")
# for contact in iterator:
#     contacts.add(contact)
#
# print("After filter: %s" % contacts.ncontacts)
#
# new_file = '/media/shah/sdc/data/atg9a/map_align/atg91_1_500.deepmetapsicov_3l_2.casp'
# conkit.io.write(new_file, "casprr", contacts)