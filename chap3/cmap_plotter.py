import pandas as pd
from bokeh.plotting import figure,show,output_file
from bokeh.models import Range1d, Legend
from bokeh.models.tools import HoverTool
from bokeh.models import ColumnDataSource
import matplotlib.pyplot as plt
import conkit.io
import conkit.plot
import conkit.io.casp
from conkit.core import Contact, ContactMap
from operator import attrgetter
from itertools import islice

##########################variables#######################

sequence_file = "/media/shah/sdc/data/re_loops/c_maps/3orgA_pdb.fasta"
sequence_format = "fasta"
contact_file = "/media/shah/sdb/db/pdbtm_nr/3org_A.pdb"
contact_format = 'pdb'
save_fig_path = "/media/shah/sdc/data/re_loops/c_maps/"
html_file = "./3org_pdbb_cmap.html"

#######format contact prediction#####################
seq = conkit.io.read(sequence_file, sequence_format).top
conpred = conkit.io.read(contact_file, contact_format).top

# Assign the sequence register to your contact prediction
conpred.sequence = seq
conpred.set_sequence_register()

# We need to tidy our contact prediction before plotting
conpred.remove_neighbors(inplace=True)
conpred.sort('raw_score', reverse=True, inplace=True)

# Finally, we don't want to plot all contacts but only the top-L,
# so we need to slice the contact cmap
cmap = conpred[:conpred.sequence.seq_len]

##################Then we can plot the cmap#############################
fig = conkit.plot.ContactMapFigure(cmap, legend=True)

fig.savefig(save_fig_path)
#######################################################################
dfObj = pd.DataFrame(columns=['id', 'res1', 'res1_chain', 'res1_seq', 'res2', 'res2_chain', 'res2_seq', 'raw_score'])

for x in cmap:
    dfObj = dfObj.append({'id':x.id, 'res1':x.res1, 'res1_chain':x.res1_chain, 'res1_seq':x.res1_seq,
                          'res2':x.res2, 'res2_chain':x.res2_chain, 'res2_seq':x.res2_seq, 'raw_score':x.raw_score}, ignore_index=True)

source = ColumnDataSource(dfObj)

output_file(html_file)

p = figure(x_range=Range1d(0, len(dfObj)), y_range=Range1d(0, len(dfObj)),
           tools = ['pan', 'wheel_zoom', 'box_zoom','reset', 'save']
           ,toolbar_location="above",
           plot_height = 575, plot_width = 700)

p1 = p.circle(x='res1_seq', y='res2_seq', size=3, color='black', source=source)
p.add_tools(HoverTool(renderers=[p1], tooltips=[('Contact', '@id'), ('res1', '@res1'),('res2', '@res2'), ('confidence', '@raw_score')]))
p1a = p.circle(x='res2_seq', y='res1_seq',  size=3, color='black', source=source)
p.add_tools(HoverTool(renderers=[p1a], tooltips=[('Contact', '@id'), ('res1', '@res1'),('res2', '@res2'), ('confidence', '@raw_score')]))


##############################

legend = Legend(items=[("Contact", [p1])], location="center")

p.add_layout(legend, 'right')
show(p)