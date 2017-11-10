import os 

from pnt_reader import get_header,get_data
from plotter import draw_pnt,draw_day_pnt,draw_colormap_pnt,colormap_day

from datetime import datetime,timedelta
from my_config import *
from calibration import get_calibration_set,calibrate
from zipper import add_hour_data_for_colormap
import cPickle as pickle
import memory_profiler

def draw_hour_pictures():

    files = os.listdir(path_to_data)
    calibration_set = get_calibration_set(calibration_file)
    os.system("mkdir "+path_to_pictures)
    k = 0
    for filename in files:
        k = k+1

        if os.path.exists(path_to_calibrated_data + filename):
            print filename + " already calibrated"
            if os.path.exists(path_to_pictures+filename[:-4]+".png"): 
                print "picture " + filename + " already exists"
            else:
                header,header_list = get_header(path_to_calibrated_data + filename)
                data = get_data(path_to_calibrated_data + filename,header)
                draw_pnt(data,header,path_to_pictures+filename[:-4]+".png")
                del data[:]
        else:
            header,header_list = get_header(path_to_data+filename)
            data = get_data(path_to_data+filename,header)
            calibrate(calibration_set,data,header,header_list,path_to_calibrated_data,filename)
            del data[:]
            data = get_data(path_to_calibrated_data + filename,header)
            draw_pnt(data,header,path_to_pictures+filename[:-4]+".png")
            del data[:]

        print filename+" done"

def draw_hour_colormap():

    files = os.listdir(path_to_data)
    calibration_set = get_calibration_set(calibration_file)
    os.system("mkdir "+path_to_colormap)
    k = 0
    for filename in files:
        k = k+1

        if os.path.exists(path_to_calibrated_data + filename):
            print filename + " already calibrated"
            if os.path.exists(path_to_colormap+filename[:-4]+".png"): 
                print "picture " + filename + " already exists"
            else:
                header,header_list = get_header(path_to_calibrated_data + filename)
                data = get_data(path_to_calibrated_data + filename,header)
                draw_colormap_pnt(data,header,path_to_colormap+filename[:-4]+".png")
                del data[:]
        else:
            header,header_list = get_header(path_to_data+filename)
            data = get_data(path_to_data+filename,header)
            calibrate(calibration_set,data,header,header_list,path_to_calibrated_data,filename)
            del data[:]
            data = get_data(path_to_calibrated_data + filename,header)
            draw_colormap_pnt(data,header,path_to_colormap+filename[:-4]+".png")
            del data[:]

        print filename+" done"
        if k> 1 :break

def draw_hour_colormap_11():

    files = os.listdir(path_to_data)
    calibration_set = get_calibration_set(calibration_file)
    os.system("mkdir "+path_to_colormap)
    k = 0

    for filename in files :
        if(filename != '140413_16_N1_000.pnt'):
            continue
        k = k+1

        if os.path.exists(path_to_calibrated_data + filename):
            print filename + " already calibrated"
            if os.path.exists(path_to_colormap+filename[:-4]+".png"): 
                print "picture " + filename + " already exists"
            else:
                header,header_list = get_header(path_to_calibrated_data + filename)
                data = get_data(path_to_calibrated_data + filename,header)
                draw_colormap_pnt(data,header,path_to_colormap+filename[:-4]+".png")
                del data[:]
        else:
            header,header_list = get_header(path_to_data+filename)
            data = get_data(path_to_data+filename,header)
            calibrate(calibration_set,data,header,header_list,path_to_calibrated_data,filename)
            del data[:]
            data = get_data(path_to_calibrated_data + filename,header)
            draw_colormap_pnt(data,header,path_to_colormap+filename[:-4]+".png")
            del data[:]

        print filename+" done"
        if k> 1 :break

def draw_day_pictures(str_day):

    files = os.listdir(path_to_data)
    calibration_set = get_calibration_set(calibration_file)
    os.system("mkdir "+path_to_all_day_pictures)
    k = 0
    added_data = [False]*24
    total_points = []
    num_of_points = 0

    for filename in files:
        k = k+1
        if filename[0:6] == str_day:
            if os.path.exists(path_to_calibrated_data + filename):
                print filename + " already calibrated"
                
                header,header_list = get_header(path_to_calibrated_data + filename)
                data = get_data(path_to_calibrated_data + filename,header)
                total_points,num_of_points,stop = draw_day_pnt(str_day,data,header,path_to_all_day_pictures+filename[0:6]+".png",added_data,total_points,num_of_points)
                del data[:]
                if stop: break
                
            else:
                header,header_list = get_header(path_to_data+filename)
                data = get_data(path_to_data+filename,header)
                calibrate(calibration_set,data,header,header_list,path_to_calibrated_data,filename)
                del data[:]
                data = get_data(path_to_calibrated_data + filename,header)
                total_points,num_of_points,stop = draw_day_pnt(str_day,data,header,path_to_all_day_pictures+filename[0:6]+".png",added_data,total_points,num_of_points)
                del data[:]
                if stop: break

            print filename+" done"

def draw_day_colormap(date_str):
    files = os.listdir(path_to_data)
    calibration_set = get_calibration_set(calibration_file)
    os.system("mkdir "+path_to_all_day_pictures)
    k = 0
    added_data = [False]*24
    total_points = []
    num_of_points = 0
    try:
        f = open('Z.pickle','rb')
        Z = pickle.load(f)
        f.close()
        colormap_day(date_str, Z,'output.png')
    except IOError:       
        Z = []
        stop = False
        for i in xrange(24):
            Z.append([])

        for filename in files:
            
            if filename[0:6] == date_str :
                k = k+1
                if os.path.exists(path_to_calibrated_data + filename):
                    print filename + " already calibrated"
                    
                    header,header_list = get_header(path_to_calibrated_data + filename)
                    data = get_data(path_to_calibrated_data + filename,header)
                    Z = add_hour_data_for_colormap(Z,data,added_data,header,date_str)
                    # total_points,num_of_points,stop = draw_day_pnt(str_day,data,header,path_to_all_day_pictures+filename[0:6]+".png",added_data,total_points,num_of_points)
                    del data[:]
                    if stop: break                
                else:
                    header,header_list = get_header(path_to_data+filename)
                    data = get_data(path_to_data+filename,header)
                    calibrate(calibration_set,data,header,header_list,path_to_calibrated_data,filename)
                    del data[:]
                    data = get_data(path_to_calibrated_data + filename,header)
                    Z = add_hour_data_for_colormap(Z,data,added_data,header,date_str)
                    # total_points,num_of_points,stop = draw_day_pnt(str_day,data,header,path_to_all_day_pictures+filename[0:6]+".png",added_data,total_points,num_of_points)
                    del data[:]
                    if stop: break
                print k
                # if k > 1 : break
        if False in added_data:
            print added_data
        else:
            f = open('Z.pickle','wb')
            pickle.dump(Z,f)
            f.close()
            colormap_day(date_str, Z,"output.png")


if __name__ == "__main__":
    
    # draw_day_pictures('140413')
    # draw_hour_pictures()
    # draw_hour_colormap()
    # draw_hour_colormap_11()
    draw_day_colormap('140413')