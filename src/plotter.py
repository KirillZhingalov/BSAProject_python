# Numpy is a library for handling arrays (like data points)
import numpy as np

# Pyplot is a module within the matplotlib library for plotting
import matplotlib.pyplot as plt

import ephem
import pytz
import matplotlib.cm as cm
from matplotlib import dates
from mpl_toolkits.mplot3d import Axes3D
from pytz import timezone
from my_config import nrays
from datetime import timedelta,datetime
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter

from matplotlib.colors import LogNorm 

def draw_pnt(data,header,output):
    #x = np.linspace(0,nrays,nrays)
    print "drawing"
    npoints = int(header["npoints"])
    date_begin_str = header["date_begin"]
    date_end_str = header["date_end"]
    time_begin_str = header["time_begin"]
    time_end_str = header["time_end"]

    o = ephem.Observer()
    o.lon = "37:37:48"

    t_begin = datetime.strptime(date_begin_str+" "+time_begin_str,"%d.%m.%Y %H:%M:%S") 

    msk = pytz.timezone("Europe/Moscow")
    t_begin.replace(tzinfo=msk)
    x = range(0,npoints)
    t_tuple = [t_begin+timedelta(seconds=i*3600*1.00/npoints) for i in x]
    s_t_tuple = []
    for t in t_tuple:
        o.date = datetime.utcfromtimestamp(float(t.strftime('%s')))
        s_t_tuple.append(datetime.strptime(str(o.sidereal_time()),"%H:%M:%S.%f"))

    
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twiny()

    plt.ylim([0,8000])

    ax2.plot(s_t_tuple,[0]*len(s_t_tuple),color = 'white',marker = '.',markersize = 0,lw = 0)
    for r in reversed(xrange(nrays)):
        c = cm.hot(r/76.,1)
        y = [(np.mean(data[i][r][0:6])+ 100*r) for i in x]
        ax1.plot(t_tuple,y,color = c,marker = '.',markersize = 0.1,lw = 0)

    
    ax2.grid(True)
    ax1.grid(True)
    ax1.set_xlabel("Moscow Time")
    ax2.set_xlabel("Star Time")
    fig.suptitle("BSA data from:" + date_begin_str)
    fig.autofmt_xdate()
    fig.set_size_inches(18.5,10.5)
    fig.savefig(output,dpi=300)

    plt.close(fig)

def draw_day_pnt(str_day,data,header,output,added_data,total_points,num_of_points):
    #x = np.linspace(0,nrays,nrays)
    print "drawing"
    npoints = int(header["npoints"])
    date_begin_str = header["date_begin"]
    date_end_str = header["date_end"]
    time_begin_str = header["time_begin"]
    time_end_str = header["time_end"]




    t_begin = datetime.strptime(date_begin_str+" "+time_begin_str,"%d.%m.%Y %H:%M:%S") 
    print (t_begin+timedelta(hours=1)).hour
    added_data[(t_begin+timedelta(hours=1)).hour] = True
    # added_data[0] = True
    x = range(0,npoints,npoints/3600)
    
    
    total_points.extend([p + num_of_points for p in x])
    num_of_points = num_of_points + npoints
    t_tuple = [t_begin+timedelta(seconds=i*3600*1.00/npoints) for i in x]

    
    fig = plt.figure(1)
    ax1 = fig.add_subplot(111)
    

    plt.ylim([0,8000])

    if False in added_data:
        pass
    else:
        ax2 = ax1.twiny()
        str_day_1 = str_day[0:4]+'20'+str_day[4:6]
        picture_time_begin = datetime.strptime(str_day_1,"%d%m%Y")
        picture_time_begin = picture_time_begin - timedelta(days = 1)
        picture_time_begin = picture_time_begin + timedelta(hours = 23)
        msk = pytz.timezone("Europe/Moscow")
        picture_time_begin.replace(tzinfo=msk)
        o = ephem.Observer()
        o.lon = "37:37:48"
        print picture_time_begin
        total_time_tuple = [picture_time_begin + timedelta(hours = 24 * i * 1.00/num_of_points) for i in total_points]
        s_t_tuple = []
        for t in total_time_tuple:
            o.date = datetime.utcfromtimestamp(float(t.strftime('%s')))
            s_t_tuple.append(datetime.strptime(str(o.sidereal_time()),"%H:%M:%S.%f"))
        plt.ylim([0,8000])
        ax2.plot(s_t_tuple,[0]*len(s_t_tuple),color = 'white',marker = '.',markersize = 0,lw = 0)

        ax2.grid(True)
        ax2.set_xlabel("Star Time")

    plt.ylim(0,8000)
    for r in reversed(xrange(nrays)):
        c = cm.hot(r/76.,1)
        y = [(np.mean(data[i][r][0:6])+ 100*r) for i in x]
        ax1.plot(t_tuple,y,color = c,marker = '.',markersize = 0.3,lw = 0)



    
    
    ax1.grid(True)
    ax1.set_xlabel("Moscow Time") 
    if(t_begin.hour != 23):
        fig.suptitle("BSA data from:" + date_begin_str)
    # fig.autofmt_xdate()
    fig.set_size_inches(18.5,10.5)



    fig.savefig(output,dpi=300)
    if False in added_data:
        pass
        print added_data
    else:
        plt.close(fig)
        return total_points,num_of_points,True
    return total_points,num_of_points,False

def draw_colormap_pnt(data,header,output):
    #x = np.linspace(0,nrays,nrays)
    print "drawing"
    npoints = int(header["npoints"])
    date_begin_str = header["date_begin"]
    date_end_str = header["date_end"]
    time_begin_str = header["time_begin"]
    time_end_str = header["time_end"]

    o = ephem.Observer()
    o.lon = "37:37:48"

    t_begin = datetime.strptime(date_begin_str+" "+time_begin_str,"%d.%m.%Y %H:%M:%S") 

    msk = pytz.timezone("Europe/Moscow")
    t_begin.replace(tzinfo=msk)
    x = range(0,npoints)
    t_tuple = [t_begin+timedelta(seconds=i*3600*1.00/npoints) for i in x]
    s_t_tuple = []
    for t in t_tuple:
        o.date = datetime.utcfromtimestamp(float(t.strftime('%s')))
        s_t_tuple.append(datetime.strptime(str(o.sidereal_time()),"%H:%M:%S.%f"))

    
    fig = plt.figure(1)
    ax1 = fig.add_subplot(111)
    # ax2 = ax1.twiny()


    # ax2.plot(s_t_tuple,[0]*len(s_t_tuple),color = 'white',marker = '.',markersize = 0,lw = 0)

    Z = []
    print data[36018][19],date_begin_str,time_begin_str
    for r in reversed(xrange(nrays)):
        

        Z.append([(np.mean(data[i][r][0:6])) for i in x])


    maxdate = matplotlib.dates.date2num(t_tuple[-1])
    mindate = matplotlib.dates.date2num(t_tuple[0])
    img = ax1.imshow(Z,cmap = cm.hot,vmin = 250,vmax=3500)#,extent=(mindate, maxdate, 0, 47))
    ax1.xaxis_date()
    hfmt = dates.DateFormatter('%H:%M:%S')
    ax1.xaxis.set_major_locator(dates.MinuteLocator(interval=10))
    ax1.xaxis.set_major_formatter(hfmt)
    ax1.set_aspect('auto')
    fig.colorbar(img) 
    # ax2.grid(True)
    # ax1.grid(True)
    # ax1.set_xlabel("Moscow Time")
    # ax2.set_xlabel("Star Time")
    # fig.suptitle("BSA data from:" + date_begin_str)
    # fig.autofmt_xdate()
    plt.show()
    fig.set_size_inches(13,6.5)
    fig.savefig(output,dpi=300)
    # plt.close(fig)
def colormap_day(str_day,Z,output):


    
    ZZ = []
    for i in xrange(24):
        ZZ.extend(Z[i])
    ZZZ = np.asarray(ZZ).T.tolist()
    fig = plt.figure(1)
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twiny()
    str_day_1 = str_day[0:4]+'20'+str_day[4:6]
    picture_time_begin = datetime.strptime(str_day_1,"%d%m%Y")
    picture_time_begin = picture_time_begin - timedelta(days = 1)
    picture_time_begin = picture_time_begin + timedelta(hours = 23)
    picture_time_end = picture_time_begin + timedelta(days = 1)
    msk = pytz.timezone("Europe/Moscow")
    picture_time_begin.replace(tzinfo=msk)
    o = ephem.Observer()
    o.lon = "37:37:48"
    print picture_time_begin

    o.date = datetime.utcfromtimestamp(float(picture_time_begin.strftime('%s')))
    sidereal_time_begin = datetime.strptime(str(o.sidereal_time())+\
        " "+str(picture_time_begin.day)+str(picture_time_begin.month)+str(picture_time_begin.year),"%H:%M:%S.%f %d%m%Y")
    o.date = datetime.utcfromtimestamp(float(picture_time_end.strftime('%s')))
    sidereal_time_end = datetime.strptime(str(o.sidereal_time())+\
        " "+str(picture_time_end.day)+str(picture_time_end.month)+str(picture_time_end.year),"%H:%M:%S.%f %d%m%Y")

    print picture_time_begin,picture_time_end
    print sidereal_time_begin,sidereal_time_end
    mindate = matplotlib.dates.date2num(picture_time_begin)
    maxdate = matplotlib.dates.date2num(picture_time_end)
    mindate_s = matplotlib.dates.date2num(sidereal_time_begin)
    maxdate_s = matplotlib.dates.date2num(sidereal_time_end)
    print maxdate_s,mindate_s
    hfmt = dates.DateFormatter('%H:%M:%S')
    print maxdate,mindate
    ax1.set_aspect('auto')
    ax2.set_aspect('auto')

    img2 = ax2.imshow(ZZZ,cmap = cm.hot,vmin = 250,vmax=3500,interpolation="bilinear",extent=(mindate_s, maxdate_s, 0, 47),aspect='auto')
    ax2.cla()
    # img2 = ax2.imshow(ZZZ,cmap = cm.hot,vmin = 250,vmax=3500,interpolation="bilinear",extent=(mindate_s, maxdate_s, 0, 47),aspect='auto')
    img = ax1.imshow(ZZZ,cmap = cm.hot,vmin = 250,vmax=3500,interpolation="bilinear",extent=(mindate, maxdate, 0, 47),aspect = "auto")
    ax1.xaxis.set_major_locator(dates.MinuteLocator(interval=150))
    ax1.xaxis.set_major_formatter(hfmt)

    

    

    ax2.xaxis.set_major_locator(dates.MinuteLocator(interval=150))
    ax2.xaxis.set_major_formatter(hfmt)
    fig.colorbar(img,orientation='horizontal',aspect = 45) 

    ax1.set_xlabel("Moscow Time")
    ax2.set_xlabel("Star Time")
    fig.suptitle("BSA data from:" + datetime.strftime(picture_time_end,"%Y.%m.%d"))
    

    fig.autofmt_xdate()
    plt.subplots_adjust(left=0.12, bottom=0.3, right=None, top=0.75, wspace=None, hspace=None)
    plt.show()

    fig.set_size_inches(13,6.5)
    fig.savefig(output,dpi=300)