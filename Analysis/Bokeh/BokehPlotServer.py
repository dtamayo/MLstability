import numpy as np
import pandas as pd
from bokeh.layouts import row, widgetbox, column
from bokeh.models import CustomJS, Slider, Select, HoverTool 
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.io import push_notebook, output_notebook, curdoc
from bokeh.client import push_session
#from bokeh.scatter_with_hover import scatter_with_hover
#output_notebook()


#Keep the shortened data for now, make it larger if this works
df_p = pd.read_csv('../../csvs/initial_orbital_elements.csv', index_col=0)
del df_p['instability_time']
del df_p['Rel_Eerr']
#del df['Rel_Eerr_short']
del df_p["runstring"]
#Nrows = df.shape[0]
#print Nrows, len(np.where(df['Stable']==0)[0])
#print df_p.shape
#df_p.head()
val_a = df_p.iloc[:3000,:]#[:200,:] #[:50, :]



# Here is a dict of some keys that I want to be able to pick from for plotting
labels = list(df_p.columns.values)
axis_map = {key:key for key in labels}

#add color and legend
colormap = {1: 'green', 0: 'blue'}
label = {1:"Stable", 0:"Unstable"}
colors = [colormap[x] for x in val_a['Stable']]
labels = [label[x] for x in val_a["Stable"]]


code2 = ''' var data = source.data;
            
           //axis values with select widgets
           var value1 = val1.value;
           var value2 = val2.value;
                     
           var original_data = original_source.data
           // get data corresponding to selection
           
           x = original_data[value1];
           y = original_data[value2];
           //data['x'] = x;
           //data['y'] = y;
           
           var start1 = Math.min.apply(Math, original_data[value1])
           var end1 = Math.max.apply(Math, original_data[value1])
           
           var start2 = Math.min.apply(Math, original_data[value2])
           var end2 = Math.max.apply(Math, original_data[value2])
           

           
           //change slider values
           slide.set("start", start1)
           slide.set("end", end1)
           slide.set("step", (end1 -start1)/20.)
           //slide.set("title", val1)
                      
           slide2.set("start", start2)
           slide2.set("end", end2)
           slide2.set("step", (end2 -start2)/20.)
           //slide2.set("title", val2)
           
           slide3.set("start", start1)
           slide3.set("end", end1)
           slide3.set("step", (end1 -start1)/20.)
           //slide3.set("title", val1+"end")
           
           slide4.set("start", start2)
           slide4.set("end", end2)
           slide4.set("step", (end2 -start2)/20.)
           //slide4.set("title", val2+"end")          
          
           
           
           //source.trigger('change');
           
           
           // set axis labels
           x_axis.axis_label = value1;
           y_axis.axis_label = value2;
           
           // #need to create filter based on min and max vals

           
           var val1 = slide.value
           var val2 = slide2.value
           var val3 = slide3.value
           var val4 = slide4.value
           
           function inBetween2X(x) {
               return (val1 < x & x < val3)

           }
           
           function inBetween2Y(x) {
               return (val2 < x & x<val4)
       
           }
           
           source.trigger('change');
           filter_x = x.filter(inBetween2X);
           filter_y = y.filter(inBetween2Y);
                  
           data['x'] = filter_x;
           data['y'] = filter_y;
                  
           
           '''


#cols = ["beta12", "beta23"]

source = ColumnDataSource(data=dict( x=val_a['RHill12'], y=val_a['RHill23'], 
                                    label = labels))
original_source = ColumnDataSource(data=val_a.to_dict(orient='list'))

TOOLS = [ HoverTool(tooltips= [(c, '@' + c) for c in val_a.columns] + [('index', '$index')])]
# hover.tooltips.append(('index', '$index'))

#plot the figures
plot = figure(plot_width=800, plot_height=800,   tools= TOOLS)
plot.scatter(x= "x",y="y", source=source, line_width=2, line_alpha=0.6, color = colors,
            legend = 'label', size = 3, name = "main")

slider = Slider(title ="Slider X Start", start=df_p['RHill12'].min(), end=df_p['RHill12'].max(),
                step=(df_p['RHill12'].max() - df_p['RHill12'].min()) /10., 
               value = df_p['RHill12'].min())
slider2 = Slider(title ="Slider Y Start", start=df_p['RHill23'].min(), end=df_p['RHill23'].max(),
                 step=(df_p['RHill23'].max() - df_p['RHill23'].min())/10., 
                 value = df_p['RHill23'].min())


slider3 = Slider(title ="Slider X End", start=df_p['RHill12'].min(), end=df_p['RHill12'].max(),
                step=(df_p['RHill12'].max() - df_p['RHill12'].min()) /10., 
               value = df_p['RHill12'].max())
slider4 = Slider(title ="Slider Y End", start=df_p['RHill23'].min(), end=df_p['RHill23'].max(),
                 step=(df_p['RHill23'].max() - df_p['RHill23'].min())/10., 
                 value = df_p['RHill23'].max())


callback = CustomJS(args=dict(source=source, original_source = original_source,
                              x_axis=plot.xaxis[0],y_axis=plot.yaxis[0], slide = slider ,
                              slide2 = slider2, slider3 =slider3,
                              slider4 = slider4), code=code2)



#create a separate callback to manage chaning data
callbackDRange = CustomJS(args = dict(source = source,original_source = original_source,
                              x_axis=plot.xaxis[0],y_axis=plot.yaxis[0], slide = slider ,
                              slide2 = slider2, slider3 =slider3,
                              slider4 = slider4), code=code2 )

slider.callback = callback
callback.args["slide"] = slider
#callbackDRange.args["slide"] = slider


slider2.callback = callback
callback.args["slide2"] = slider2
#callbackDRange.args["slide2"] = slider2

slider3.callback = callback
callback.args["slide3"] = slider3
#callbackDRange.args["slide3"] = slider3

slider4.callback = callback
callback.args["slide4"] = slider4
#callbackDRange.args["slide4"] = slider4


#Create two select widgets to pick the features of interest 
x_axis = Select(title="X Axis", options=sorted(axis_map.keys()), value="RHill12", callback = callback)
callback.args["val1"] = x_axis
callbackDRange.args["val1"]= x_axis

y_axis = Select(title="Y Axis", options=sorted(axis_map.keys()), value="RHill23", callback = callback)
callback.args["val2"] = y_axis
callbackDRange.args["val2"]= y_axis

y_axis.js_on_change("value", callback)

x_axis.js_on_change("value", callback)


plot.xaxis[0].axis_label = 'RHill12'
plot.yaxis[0].axis_label = 'RHill23'
#Error message due to legend, need to find a better way to do so


layout = column(plot, x_axis, y_axis, row(slider, slider2),row(slider3, slider4) )

curdoc().add_root(layout)
