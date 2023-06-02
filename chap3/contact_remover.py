import conkit.io
import conkit.plot
import conkit.io.casp
from conkit.core import Contact, ContactMap
from operator import attrgetter
from itertools import islice


sequence_file = "/media/shah/sdc/data/w9dy28/5lil/5lil_full.fasta"
sequence_format = "fasta"
contact_file = "/media/shah/sdc/data/w9dy28/5lil/MP003514_results/cont.txt"
contact_format = "nebcon"

seq = conkit.io.read(sequence_file, sequence_format).top
conpred = conkit.io.read(contact_file, contact_format).top

print('Sequence length = ' + str(len(seq)))

print("Before filter: %s" % conpred.ncontacts)

# #Filter out contacts
pre_filtered_map=ContactMap("my_map_prefiltered")
for contact in conpred:
    seq_distance=abs(int(contact.res1_seq)-int(contact.res2_seq))
    if (seq_distance > 12) and (contact.raw_score > 0.1): #!!!!!!check!!!!!
        pre_filtered_map.add(contact)

filtered_map=ContactMap("my_map_filtered")
for contact in pre_filtered_map:
    if (contact.res1_seq >240 and contact.res2_seq >240):
        filtered_map.add(contact)

iterator = islice(filtered_map, 306,503)
iterator = sorted(iterator, key=attrgetter('res1_seq'))
contacts = ContactMap("my_map_filtered2")

for x in filtered_map:
    if (x.res1_seq <306) or (x.res1_seq >503):
        contacts.add(x)

for contact in contacts:
    print(contact)

fig = conkit.plot.ContactMapFigure(contacts, legend=True)
fig.savefig("/media/shah/sdc/data/w9dy28/5lil/MP003514_results/5lil_map_pred_filtered.png")
