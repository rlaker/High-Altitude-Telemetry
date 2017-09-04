# -*- coding: utf-8 -*-
"""
Created on Fri Sep 01 17:50:27 2017

@author: Ronan
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import numpy as np
import re
import matplotlib.dates as md
import datetime
import time
import pandas as pd
import simplekml
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw



file_text  = open('telemetry.txt', 'r')
text = file_text.read()

split_instruction = re.compile(',')
split_text =split_instruction.split(text)


separation = 17
length = len(split_text)
n = length/separation
n = np.ceil(n)
i = 0

number= []
time = []
gps_long = []
gps_lat = []
altitude = []
speed = []
direction = []
satellites = []
internal_temp = []
voltage = []
current = []
temp_bme = []
pres = []
hum = []
uva = []
uvb = []
sound=[]

print length

while i < length:
    if i > (length-16):
        break
    #goes through file and adds each variable to the right list, the last variable needs seperating from the callsign
    number.append(split_text[1+i])
    time.append(split_text[2+i])
    gps_long.append(split_text[4+i])
    gps_lat.append(split_text[3+i])
    altitude.append(split_text[5+i])
    speed.append(split_text[6+i])
    direction.append(split_text[7+i])
    satellites.append(split_text[8+i])
    internal_temp.append(split_text[9+i])
    voltage.append(split_text[10+i])
    current.append(split_text[11+i])
    temp_bme.append(split_text[12+i])
    pres.append(split_text[13+i])
    hum.append(split_text[14+i])
    uva.append(split_text[15+i])
    uvb.append(split_text[16+i])
    sound.append(split_text[17+i])
    i = i + separation

def fix_list(x):
    for i in np.arange(0,len(x)):
        if x[i][1] == '.':
            x[i]=x[i][0:3]
        elif x[i][2] == '.':
            x[i]=x[i][0:4]
        else:
            x[i]=x[i][0:5]
    return x
    
def plot_3d(X,Y,Z,zlabel):
    X = [ float(x) for x in X ]
    Y = [ float(x) for x in Y ]
    Z = [ float(x) for x in Z ]
    fig = plt.figure()
    ax1 = fig.add_subplot(111, projection='3d')
    ax1.plot_wireframe(X,Y,Z)
    ax1.set_xlabel('Latitiude')
    ax1.set_ylabel('Longitude')
    ax1.set_zlabel(zlabel)

    """plt.figure(8)
    plt.plot(gps_long,gps_lat)
    plt.xlabel('Long')
    plt.ylabel('Lat')"""  

def plot_variable(x,y,xlabel,ylabel):
    plt.plot(x,y)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

def fix_time():
    fixed_time_list = []
    for i in time:
        
        hour = int(i[0:2])
        mins = int(i[3:5])
        secs = int(i[6:8])
        fixed_time = datetime.datetime(2017, 8, 19, hour, mins, secs)
        fixed_time_list.append(fixed_time)
    return fixed_time_list
    
def get_uv_ratio(uva,uvb):
    uv_ratio = []
    uva = [ float(x) for x in uva ]
    uvb = [ float(x) for x in uvb ]
    for i in np.arange(len(uva)):
        if uva[i] != 0:
            uv_ratio_single = uvb[i]/uva[i]
            if uv_ratio_single > 100:
                uv_ratio_single = uv_ratio_single/10
            uv_ratio.append(uv_ratio_single)
        else:
            uv_ratio.append(0)
        
    return uv_ratio
    
    
def open_image(hours, mins, secs):
    image_secs = secs
    image_mins = mins
    if len(str(image_secs)) == 1:
                    image_secs = '0' + str(secs)
                    
    if len(str(image_mins)) == 1:
                    image_mins = '0' + str(image_mins)
    
    image = Image.open(str(hours) + '_' + str(image_mins) + '_' + str(image_secs) + '.jpg')    
    return image, image_mins, image_secs


    
    

def data_for_picture(hours, mins, secs):
    
        
    #finds the data for the nearest time to the picture
    # i.e. a picture taken at 18:40:32 but data taken at 18:40:34    
    
    open_image(hours, mins, secs)    
    
    for i in np.arange(len(time)):
        if time[i][0:2] == str(hours):
            if len(str(mins)) == 1:
                    mins = '0' + str(mins)
            if time[i][3:5] == str(mins):
                list_of_secs = []
                if (len(time)-i) <= 6:
                    for j in np.arange(0,len(time)-i):
                        
                        
                        list_of_secs.append(int(time[j+i][6:8]))
                    
                        
                else:
                    for j in np.arange(0,11):
                        
                        list_of_secs.append(int(time[j+i][6:8]))
                        
                list_of_secs.append(secs)
                list_of_secs.sort()
                i = list_of_secs.index(secs)
                
                #print i, list_of_secs, time
                
                if i != len(list_of_secs)-1:      
                    
                    above = int(list_of_secs[i+1]) - int(secs)
                    below =  int(secs) - int(list_of_secs[i-1])
        
                
                    if above > below:
                        secs = int(list_of_secs[i-1])
                        
                    if above < below:
                        secs = int(list_of_secs[i+1])
                    if above == below:
                        secs = int(list_of_secs[i+1])
                
                
                if len(str(secs)) == 1:
                    secs = '0' + str(secs)
    
                string = str(hours) + ':' + str(mins) + ':' + str(secs)
                i = time.index(string)
                
                print 'Nearest Time', time[i]
                print 'Altitude', altitude[i]
                print 'Internal Temp', internal_temp[i]
                print 'External Temp', temp_bme[i]
                print 'Pressure', pres[i]
                print 'Humidity', hum[i]
                print 'UVA', uva[i]
                print 'UVB', uvb[i]
                print 'Sound', sound[i]
                print 'Co-ordinates', gps_lat[i], gps_long[i]
                
                plot_variable(gps_lat, gps_long, 'Lat','Long')
                plt.scatter(gps_lat[i], gps_long[i], s=200, color = 'r', marker='+', linewidth = 2)
                
                
                return time[i], altitude[i], internal_temp[i], temp_bme[i], pres[i], hum[i], uva[i], uvb[i], sound[i], gps_lat[i],gps_long[i]
    
def data_on_image(hours, mins, secs):
    
    #prints data on image     
    
    img = open_image(hours, mins, secs)    
    draw = ImageDraw.Draw(img[0])

    font = ImageFont.truetype("Verdana.ttf",50)
    
    stats = data_for_picture(hours, mins, secs)
    
    string1 = 'Time:   ' + stats[0]
    string2 = 'Altitude:   ' + stats[1]
    string3 = 'Internal Temp:   ' + stats[2]
    string4 = 'External Temp:   ' + stats[3]
    string5 = 'Pressure:   ' + stats[4]
    string6 =  'Humidity:   ' + stats[5]
    string7 =  'UVA:   ' + stats[6]
    string8 =  'UVB:   ' + stats[7]
    string9 =  'Sound:   ' + stats[8]
    string10 =  'Co-ordinates:   ' + stats[9] + ', ' + stats[10]
    
    colour = (256,256,256)
    top = 1200
    
    draw.text((0, top),string1,colour,font=font)
    draw.text((0, top+70),string2,colour,font=font)
    draw.text((0, top+140),string3,colour,font=font)
    draw.text((0, top+210),string4,colour,font=font)
    draw.text((0, top+280),string5,colour,font=font)
    draw.text((0, top+350),string6,colour,font=font)
    draw.text((0, top+420),string7,colour,font=font)
    draw.text((0, top+490),string8,colour,font=font)
    draw.text((0, top+560),string9,colour,font=font)
    draw.text((0, top+630),string10,colour,font=font)
    
    img[0].save(str(hours) + '_' + str(img[1]) + '_' + str(img[2]) + '_with_data' + '.jpg')
    


def plot_all(x, xlabel):
    
    #plots all graphs    
    
    plt.figure(1)
    plt.subplot(211)
    plt.plot(x,internal_temp)
    plt.xlabel(xlabel)
    plt.ylabel('Internal Temp / Celcius')
    plt.subplot(212)
    plt.plot(x,temp_bme)
    plt.xlabel(xlabel)
    plt.ylabel('Outside Temp / Celcius')
    plt.figure(2)
    plt.plot(x,pres)
    plt.xlabel(xlabel)
    plt.ylabel('Pressure / kPa')
    #plt.ylim(100.5,100.9)
    plt.figure(3)
    plt.plot(x,hum)
    plt.xlabel(xlabel)
    plt.ylabel('Humidity / %')
    plt.figure(4)
    plt.plot(x,uva, 'r', label = 'UVA')
    plt.plot(x,uvb, 'b', label= 'UVB')
    plt.legend()
    plt.xlabel(xlabel)
    plt.ylabel('UVA')
    plt.figure(5)
    plt.plot(x,sound)
    plt.xlabel(xlabel)
    plt.ylabel('Speed of Sound / ms^-1')
    plt.figure(6)
    plt.plot(x,satellites)
    plt.xlabel(xlabel)
    plt.ylabel('Satellites')
    plt.figure(7)
    plt.plot(x,altitude)
    plt.xlabel(xlabel)
    plt.ylabel('Altitude')
    plt.figure(8)
    plt.plot(gps_long,gps_lat)
    plt.xlabel('Long')
    plt.ylabel('Lat')
    plt.figure(9)
    plt.plot(x,voltage)
    plt.xlabel(xlabel)
    plt.ylabel('Voltage')
    plt.figure(10)
    plt.plot(x,current)
    plt.xlabel(xlabel)
    plt.ylabel('Current')
    
    uv_ratio = get_uv_ratio(uva,uvb)
    plt.figure(11)
    plt.plot(x,uv_ratio)
    plt.xlabel(xlabel)
    plt.ylabel('UVB/UVA')
    
def plot_all3d():   
    plot_3d(gps_lat,gps_long,altitude, 'Altitude')
    plot_3d(gps_lat,gps_long,internal_temp, 'Internal Temp')
    plot_3d(gps_lat,gps_long,temp_bme, 'External Temp')
    plot_3d(gps_lat,gps_long,pres, 'Pressure')
    plot_3d(gps_lat,gps_long,hum, 'Humidity')
    plot_3d(gps_lat,gps_long,sound, 'Speed of Sound')
    plot_3d(gps_lat,gps_long,uva, 'UVA')
    plot_3d(gps_lat,gps_long,uvb, 'UVB')

def export_pins_google_earth(gps_lat,gps_long,altitude):
    
    ##exports points to kml so it can be seen on google earth    
    
    kml = simplekml.Kml()
    for i in np.arange(len(gps_long)):
        kml.newpoint(coords=[(gps_long[i],gps_lat[i],altitude[i])])
    kml.save(path = "pins_hill.kml")
    
    
def export_lines_google_earth_alt(gps_lat,gps_long,altitude):
    
    ## exports as lines with an altitude to visualise the flight    
    
    kml = simplekml.Kml(open=1)
    for i in np.arange(len(gps_long)-1):
        linestring = kml.newlinestring(name="Balloon Path")
        linestring.coords = [(gps_long[i],gps_lat[i],altitude[i]), (gps_long[i+1],gps_lat[i+1],altitude[i+1])]
        linestring.altitudemode = simplekml.AltitudeMode.relativetoground
        linstring.style.linestyle.color = 'ff0000ff'
        linestring.extrude = 1
    kml.save(path = "lines_alt_hill.kml")


def export_lines_google_earth(gps_lat,gps_long):
    kml = simplekml.Kml(open=1)
    for i in np.arange(len(gps_long)-1):
        linestring = kml.newlinestring(name="Balloon Path")
        linestring.coords = [(gps_long[i],gps_lat[i], 2), (gps_long[i+1],gps_lat[i+1],2)]
        linestring.altitudemode = simplekml.AltitudeMode.relativetoground
        linestring.style.linestyle.color = 'ff0000ff'
        linestring.extrude = 1
    kml.save(path = "lines_hill.kml")

fix_list(sound)
fixed_time_list = fix_time()


#print uva,uvb
#plot_variable(altitude[:351],pres[:351], 'Altitude', 'Pressure')

#plot_all(fixed_time_list, 'Time')
#plot_all(number, 'Time')

#plot_all3d()

#data_for_picture(18,04,57)

#export_lines_google_earth(gps_lat,gps_long, altitude)

#export_lines_google_earth(gps_lat,gps_long)

data_on_image(17,18,40)

plt.show()
