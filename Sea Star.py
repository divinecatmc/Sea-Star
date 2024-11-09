import csv
from bokeh.plotting import show,figure
from bokeh.palettes import Category20c
from bokeh.transform import cumsum
from math import pi
import pandas as pd
import numpy as np
import random

def piechart(x,y,listofdata):

    total = sum(listofdata)
    
    listofdata.insert(0,0)

    data_array = np.array(listofdata)

    data_angles = data_array*2*pi/total

    anglescum = np.cumsum(data_angles)

    for i in range(len(anglescum)-1):
        f.annular_wedge(x,y,0,1,anglescum[i],anglescum[i+1],color=(random.randint(1,255),random.randint(1,255),0))



sites = []

samplesize = {}

roe = 0

samples = 0
healthy = 0
mild = 0
severe = 0


years = {}

time = []

f = figure(x_range=[0,4],y_range=[0,4])

g = figure()

ex = 0
why = 0

percents = {}
with open("molly_sultany_ssws.csv") as csv_file:

    csv_reader = csv.reader(csv_file, delimiter=",")

    for row in csv_reader:

        if roe != 0:

            if row[2] not in sites:

                samplesize[row[2]] = [samples,healthy,mild,severe]

                samples = 0

                healthy = 0

                mild = 0

                severe = 0
                sites.append(row[2])
                

            samplesize[row[2]][0] += int(row[13])

            if row[11] == "healthy":

                samplesize[row[2]][1] += int(row[13])
            
            if row[11] == "mild":

                samplesize[row[2]][2] += int(row[13])

            if row[11] == "severe":
                
                samplesize[row[2]][3] += int(row[13])
            
            months = row[6].split("/")[0]

            year = row[6].split("/")[2]

            if year not in time:

                time.append(year)

                years[year] = {}

                years[year]['total'] = 0

                years[year]['healthy'] = 0

                years[year]['mild'] = 0

                years[year]['severe'] = 0
            
            else:

                years[year]['total'] += int(row[13])

                if row[11] == "healthy":

                    years[year]['healthy'] += int(row[13])
                
                if row[11] == "mild":

                    years[year]['mild'] += int(row[13])
                
                if row[11] == "severe":

                    years[year]['severe'] += int(row[13])
                    
        roe += 1

    healthies = []
    

    for yer in time:
        
        percents[yer] = {}

        percents[yer]['healthy'] = round(years[yer]['healthy'] / years[yer]['total']*100,2)
        health = percents[yer]['healthy']

        percents[yer]['mild'] = round(years[yer]['mild'] / years[yer]['total']*100,2)
        mil = percents[yer]['mild']

        percents[yer]['severe'] = round(years[yer]['severe'] / years[yer]['total']*100,2)
        sever = percents[yer]['severe']

        healthies.append(health)

        piechart(ex,why,[health,mil,sever])

        f.text(text=[str(yer)],x=ex-0.125,y=why-1.2)
        f.text(text=['healthy: ' +str(health) + '%'],x=ex-0.25,y=why-1.5)
        f.text(text=['mild: ' + str(mil) + '%'],x=ex-0.25,y=why-1.75)
        f.text(text=['severe: ' + str(sever) + '%'],x=ex-0.25,y=why-2)
        f.text(text=['sample size: ' + str(years[yer]['total'])],x=ex-0.25,y=why-2.25)
        ex += 3


#g.line(x=time,y=healthies)




print(samplesize)
print(years)
csv_file.close()

show(f)
