import pandas as pd
import numpy as np
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, Range1d, LabelSet, Label, CategoricalColorMapper
from bokeh.palettes import RdBu3

#output_file("label.html", title="label.py example")

data = pd.read_csv('/media/shah/sdc/data/tmem41b/dali/ros_map_pred/test_hit_cnt.txt', sep = '\t',names = ["pdb", "mean_z", "No_hits", "dali_des"])

df_length=len(data)

for i in range(0,df_length):data.loc[i, "hit_z_sum"] = np.sum(data.iloc[i, 1:2])
data.loc[(data.mean_z >4) & (((data.No_hits) > 10)), 'PASS'] = 'TRUE'
data['PASS'].fillna('FALSE', inplace=True)

data_series1 = data.loc[(data.PASS == 'TRUE')]
data_series2 = data.loc[(data.PASS == 'FALSE')]

print(data_series1)

x = data.iloc[:,1].tolist()
y = data.iloc[:,2].tolist()
labels = data.iloc[:,0].tolist()
sums =  data.iloc[:,4].tolist()
color= data.iloc[:,5].tolist()

source = ColumnDataSource(data=dict(x_values=x,y_values=y,label_values=labels,sums_values=sums, color_values=color,))

color_mapper = CategoricalColorMapper(factors=['TRUE', 'FALSE'], palette=[RdBu3[2], RdBu3[0]])

p = figure(title='Dali Hits',
           x_range=Range1d(2, 10), y_range=Range1d(0, 30))
p.scatter(x='x_values', y='y_values', size=8, source=source, color={'field': 'color_values', 'transform': color_mapper})
p.xaxis[0].axis_label = 'Mean Z score'
p.yaxis[0].axis_label = 'Number of Hits/41'

# labels = LabelSet(x='x_values', y='y_values', text='label_values', level='glyph',
#                x_offset=5, y_offset=5, source=source, render_mode='canvas')
#
# citation = Label(x=70, y=70, x_units='screen', y_units='screen',
#                   text='Test', render_mode='css',
#                   border_line_color='black', border_line_alpha=1.0,
#                   background_fill_color='white', background_fill_alpha=1.0)
#
# # p.add_layout(labels)
# p.add_layout(citation)

show(p)
