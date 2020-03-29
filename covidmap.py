# Libraries
#https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series
import pandas as pd
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import imageio as io
import os
from matplotlib.lines import Line2D


covid = pd.read_csv("https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
covid_d = pd.read_csv("https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")

#Check if img folder exists; if not, create it
if not os.path.exists('img'):
    os.makedirs('img') 

### CREATE ALL IMAGES
for d in range(4,covid.iloc[1,:].size):
    print('Plotting Fig '+str(d))
    
    # Set the dimension of the figure
    my_dpi=96
    plt.figure(figsize=(2600/my_dpi, 1800/my_dpi), dpi=my_dpi)
    
    # Make the background map
    m=Basemap(llcrnrlon=-180, llcrnrlat=-65,urcrnrlon=180,urcrnrlat=80)
    m.drawmapboundary(fill_color='#A6CAE0', linewidth=0)
    m.fillcontinents(color='grey', alpha=0.3)
    m.drawcoastlines(linewidth=0.1, color="white")
     
    
     
    # Add a point per position
    m.scatter(x=covid["Long"], y=covid["Lat"], s=covid[covid.iloc[:,d].name], alpha=0.4, color='yellow')
    m.scatter(x=covid_d["Long"], y=covid_d["Lat"], s=covid_d[covid_d.iloc[:,d].name], alpha=0.4, color='red')
    
    
    #Totals
    totalc = covid[covid.iloc[:,d].name].sum()
    totald = covid_d[covid_d.iloc[:,d].name].sum()
    
    # Text
    plt.text( -177, -40,'COVID-19 Confirmed Cases/Deaths', ha='left', va='bottom', size=23, color='#555555' )
    plt.text( -177, -45,covid.iloc[:,d].name, ha='left', va='bottom', size=10, color='#555555' )
    
    legend = [Line2D([0], [0], marker='o', color='w', label='Cases: '+str(totalc),
                          markerfacecolor='yellow', markersize=15),
              Line2D([0], [0], marker='o', color='w', label='Deaths: '+str(totald),
                          markerfacecolor='red', markersize=15)]
    # plt.text( -170, -50,'Casos:'+str(totalc), ha='left', va='bottom', size=10, color='#555555' )
    # plt.text( -170, -55,'Muertes:'+str(totald), ha='left', va='bottom', size=10, color='#555555' )
    
    plt.legend(handles=legend, loc=(0,0))
    # Save as png
    filename = str(d/10) + '.png'
    plt.savefig('img/'+filename, bbox_inches='tight')
    plt.clf()
    
    
### CREATE GIF
images = []
for file_name in sorted(os.listdir('img/')):
    if file_name.endswith('.png'):
        images.append(io.imread('img/'+file_name))
        
#ADD END FRAMES
for i in range(20):
    images.append(images[-1])
    
#Save GIF
io.mimsave('animated.gif', images,fps=5)
