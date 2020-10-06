#Import libraries
import pandas
from bokeh.plotting import figure, show, output_file
from capture import df
from bokeh.models import HoverTool, ColumnDataSource

df['Start_string'] = df['Start'].dt.strftime('%Y-%m-%d %h %m %s')
df['End_string'] = df['End'].dt.strftime('%Y-%m-%d %h %m %s')
cds = ColumnDataSource(df)

p = figure(x_axis_type = 'datetime', height = 300, width  = 800, 
title = 'Motion Sensor Graph')

#Define hovering tools
hover = HoverTool(tooltips = [("Start" , "@Start_string"),("End", "@End_string")])
p.add_tools(hover)
q = p.quad(left = 'Start', right = 'End', top = 1, 
bottom = 0, color = 'green', source = cds)

#Save html graph and display it
output_file('Graph.html')
show(p)
