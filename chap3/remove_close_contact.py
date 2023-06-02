
# Import
import conkit.io, conkit.io.casp
from conkit.core import Contact, ContactMap
from operator import attrgetter
from itertools import islice

#Read map
my_map = conkit.io.read('/media/shah/sdc/data/atg9a/dmp/1_500/atg91_1_500.deepmetapsicov.con', 'nebcon').top_map
print("Before filter: %s" % my_map.ncontacts)

#Filter out contacts
filtered_map=ContactMap("my_map_filtered")
for contact in my_map:
    seq_distance=abs(int(contact.res1_seq)-int(contact.res2_seq))
    if (seq_distance > 12) and contact.raw_score>0.9: #filters contacts <12 aa apart AND score <0.9
        filtered_map.add(contact)

print("After filter: %s" % filtered_map.ncontacts)

new_file = '/media/shah/sdc/data/atg9a/map_align/atg91_1_500.deepmetapsicov3.casp'
conkit.io.write(new_file, "casprr", filtered_map)

