
from datetime import datetime,timedelta

from my_config import nrays

import numpy as np

def add_hour_data_for_colormap(Z,data,added_data,header,date_str):

    print "zipping"
    npoints = int(header["npoints"])
    date_begin_str = header["date_begin"]
    date_end_str = header["date_end"]
    time_begin_str = header["time_begin"]
    time_end_str = header["time_end"]

    t_begin = datetime.strptime(date_begin_str+" "+time_begin_str,"%d.%m.%Y %H:%M:%S") 
    print (t_begin+timedelta(hours=1)).hour

    this_hour = (t_begin+timedelta(hours=1)).hour

    added_data[this_hour] = True

    step = npoints/3600
    i = -1
    
    for n in xrange(0,npoints,step):
        i = i+1
        Z[this_hour].append([])
        for r in xrange(nrays):
            Z[this_hour][i].append([])
            for k in range(n,(min(n+step,npoints)-1)):
                Z[this_hour][i][r].append(np.mean(data[k][r]))
            Z[this_hour][i][r] = np.mean(Z[this_hour][i][r])
    return Z

