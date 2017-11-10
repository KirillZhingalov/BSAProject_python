# -*- coding: utf-8 -*-
import re
import time
import operator
from datetime import datetime,timedelta
from my_config import nrays
from pnt_reader import write_pnt_data
parts = [                          
    r'\s*(?P<equivalent_id>[0-9]+)\s*\|',                 # time [02/Jun/2013:07:03:19 +0400]
    r'\s*(?P<files_id>[0-9]+)\s*\|', 
    r'\s*(?P<index_pnt_in_file>[0-9]+)\s*\|',
    r'\s*(?P<time>[^ ]* [^ ]*)\s*\|',
    r'\s*(?P<time_in_MJD>[0-9.]+)\s*\|',
    r'\s*(?P<alpha>[0-9.]+)\s*\|',
    r'\s*(?P<type_of_equivalent>[0-9.]+)\s*\|',
    r'\s*(?P<scale_in_K_Temp>[0-9.]+)\s*\|',
    r'\s*(?P<usability>[0-9.]+)\s*\|'                             
]
pattern = re.compile(r''.join(parts))
array_pattern = re.compile('{([^\| ]+)}')

class Calibration_Signal:
    """
    Строение таблицы эквивалентов в базе данных:
    TABLE Equivalents (
    equivalent_id         INTEGER PRIMARY KEY DEFAULT NEXTVAL('equivalent_id_seq'),
    files_id              INTEGER,
    index_pnt_in_file     INTEGER,
    time                  timestamp NOT NULL,
    time_in_MJD           double precision,
    Alpha                 float,
    type_of_equivalent    integer,
    scale_in_K_Temp       float,
    usability             float,
    cnl_001               float[],
    cnl_002               float[],
    ...
    cnl_128               float[]
    );


    Здесь:
    equivalent_id  - индекс конкретной записи в таблице Equivalents - вряд
    ли Вам пригодится

    files_id - номер файла в базе данных, с которого сняты
    калибровочные сигналы эквивалентов - не думаю, что особо нужно...

    index_pnt_in_file - номер индекса внутри файла, с которого начинается
    сигнал эквивалента - это Вам уже может пригодиться
    Всего подается тройка сигналов:
    1) с температурой окружающей среды - условно, 278 Кельвин - т.н.
    "ноль" - подается 5 секунд
    2) с генератора шума (т.н. "ступенька") - мощностью 2400 Кельвин -
    подается 5 секунд 
    3) с температурой окружающей среды - условно, 278 Кельвин - т.н.
    "ноль" - подается 5 секунд

    time , time_in_MJD , Alpha - московское время, юлианские дни в
    системе MJD (отсчитываются, если правильно помню, с 1-го января 1870
    года), звездное время. Что-то из этого - точно понадобится, ходя бы
    для интерполяции по времени (разумеется, удобнее всего time_in_MJD)

    $type_of_equivalent :
    =0 - нулевой эквивалент с температурой 278 кельвин - примерная среднегодовая температура в Пущино
    =1 - эквивалент-ступенька с температурой 2400 кельвин

    scale_in_K_Temp - соотвественно, 278 (на самом деле плавает и равно
    температуре на улице) или 2400 кельвин.

    usability  - пока не используется, сейчас везде 1 - подразумевается, что 1 -
    используется, 0 - плохой эквивалент, не использовать


    cnl_NNN - номер канала с многолучевой диаграммы БСА3. Сейчас
    задействованы с 33 по 128 каналы, а первые 32 - пустые. В принципе,
    есть таблица , где лежат данные, когда в какой день какие каналы
    работают, но пока Вам достаточно сказанного - с 33 по 128 каналы содержат
    данные в виде массивов float[] , в котором лежат: калибровочные
    сигналы по всем полосам (в нашем случае - с 12 по 15 апреля - 6 посос)
    + одна общая (именно это значение для нас обычно главное).
    """

    def __init__(self,groupdict):
        self.equivalent_id = groupdict['equivalent_id']
        self.files_id = groupdict['files_id']
        self.index_pnt_in_file = groupdict['index_pnt_in_file']
        self.time = groupdict['time']
        self.time_in_MJD = groupdict['time_in_MJD']
        self.alpha = groupdict['alpha']
        self.type_of_equivalent = groupdict['type_of_equivalent']
        self.scale_in_K_Temp = groupdict['scale_in_K_Temp']
        self.usability = groupdict['usability']
        self.signal = groupdict['signal']

def get_calibration_set(filename):

    calib_signals = []

    f = open(filename,"r")
    lf = open('calibration.log',"w")
    fc = open('calibration_set.dat','w')
    f.readline()
    f.readline()

    for line in f:
        try:
            temp_calib_dict = get_calib_dict(line)
            calib_signals.append(Calibration_Signal(temp_calib_dict))
        except:
            lf.write("Parsing error with this string : "+line)
    lf.close()
    for s in calib_signals:
        fc.write(str(s.time) + "\n")
    fc.close()
    return calib_signals

def get_calib_dict(line):
    res = pattern.match(line).groupdict()
    res['equivalent_id'] = int(res['equivalent_id'])
    res['files_id'] = int(res['files_id'])
    res['index_pnt_in_file'] = int(res['index_pnt_in_file'])
    res['time'] = datetime.strptime(res['time'],'%Y-%m-%d %H:%M:%S.%f')
    res['time_in_MJD'] = float(res['time_in_MJD'])
    res['alpha'] = float(res['alpha'])
    res['type_of_equivalent'] = int(res['type_of_equivalent'])
    res['scale_in_K_Temp'] = float(res['scale_in_K_Temp'])
    res['usability'] = float(res['usability'])
    res['signal'] = [x.replace(' ','').split(',') for x in array_pattern.findall(line)]
    if(len(res['signal']) != 96):
        raise Calib_signal_exception
    return res

def calibrate(calibration_set,data,header,header_list,path_to_calib,filename):
    """
    Как калибровать?
    Нужно взять сигнал "ступеньки"
    Stup_current_time__total_band__in_cannel в общей полосе в соответствующем канале и
    "ноль" Null_current_time__total_band__in_cannel в общей полосе в соотвествующем канале - на конкретное нужное время
    (в общем случае интерполировать между соседними значениями на нужное
    время) и, откалибровать сигнал по формуле:

    Sygnal_calb=(Sygnal_first - Zero) / one_Kelvin ;
    где:

    one_Kelvin=(Stup_current_time__total_band__in_cannel -
    Null_current_time__total_band__in_cannel) / (2400-278);
    Zero= Null_current_time__total_band__in_cannel - one_Kelvin*278;

    """
    print "calibration"
    npoints = int(header["npoints"])
    date_begin_str = header["date_begin"]
    date_end_str = header["date_end"]
    time_begin_str = header["time_begin"]
    time_end_str = header["time_end"]
    nbands = int(header["nbands"])+1

    t_begin = datetime.strptime(date_begin_str+" "+time_begin_str,"%d.%m.%Y %H:%M:%S")
    t_end = t_begin + timedelta(hours = 1)

    need_calibration_set = []

    # for x in calibration_set : print x.time
     
    if calibration_set[0].time > t_begin and calibration_set[0].time < t_end:
            need_calibration_set.append(calibration_set[0])
    if calibration_set[-1].time > t_begin and calibration_set[-1].time < t_end:
            need_calibration_set.append(calibration_set[-1])
    for i in xrange(1,len(calibration_set)-1):
        if calibration_set[i].time > t_begin and calibration_set[i].time < t_end:
            need_calibration_set.append(calibration_set[i])
        if calibration_set[i].time < t_begin and calibration_set[i+1].time > t_begin:
            need_calibration_set.extend([calibration_set[i],calibration_set[i-1]])
        if calibration_set[i].time > t_end and calibration_set[i-1].time < t_end:
            need_calibration_set.extend([calibration_set[i],calibration_set[i+1]])

    print t_begin,t_end
    if t_end > need_calibration_set[-1].time:
        print "cannot calibrate this data"
        return
    for i in need_calibration_set:
        print i.time
    need_calibration_set.sort(key= lambda x: x.time)
    need_calibration_set_hot = []
    need_calibration_set_cool = []
    for c in need_calibration_set:
        if c.type_of_equivalent == 0:
            need_calibration_set_cool.append(c)
        else :
            need_calibration_set_hot.append(c)  
    print t_begin
    print t_end
    time_point = [t_begin+timedelta(seconds = 3600*x/npoints) for x in xrange(npoints)]


    res_data = []

    ht = need_calibration_set_hot[0].scale_in_K_Temp

    for t in xrange(npoints):
        time = time_point[t]
        index = 0
        for i in xrange(1,len(need_calibration_set_hot)):
            if ( time < need_calibration_set_hot[i].time ) and (time > need_calibration_set_hot[i-1].time):
                index = i-1
                break
        cool_temp_difference = need_calibration_set_cool[index+1].scale_in_K_Temp - need_calibration_set_cool[index].scale_in_K_Temp
        time_between_calibration = (need_calibration_set_hot[index+1].time - need_calibration_set_hot[index].time).seconds*1000000 + (need_calibration_set_hot[index+1].time- need_calibration_set_hot[index].time).microseconds*1.00 
        res_data.append([])
        if (time > need_calibration_set[index].time):
            dt = ((time - need_calibration_set_cool[index].time).seconds*1000000 + (time - need_calibration_set_cool[index].time).microseconds*1.00)
        else:
            dt = ((need_calibration_set_cool[index].time - time).seconds*1000000 + (need_calibration_set_cool[index].time -time).microseconds*1.00)

        for r in xrange(nrays):
            res_data[t].append([])
            for b in xrange(nbands):

                hot_signal_difference = float(need_calibration_set_hot[index+1].signal[r][b]) - float(need_calibration_set_hot[index].signal[r][b])

                hs = float(need_calibration_set_hot[index].signal[r][b]) + \
                    (hot_signal_difference) / (time_between_calibration) * dt 

                cool_signal_difference = float(need_calibration_set_cool[index+1].signal[r][b]) - float(need_calibration_set_cool[index].signal[r][b])

                cs = float(need_calibration_set_cool[index].signal[r][b]) + \
                    (cool_signal_difference) / (time_between_calibration) * dt       

                ct = float(need_calibration_set_cool[index].scale_in_K_Temp) + \
                     cool_temp_difference / time_between_calibration * dt 

                one_Kelvin = (hs - cs)/(ht - ct)
                Zero = cs - one_Kelvin*ct 
                res_data[t][r].append((data[t][r][b] - Zero)/one_Kelvin)   

    del need_calibration_set_cool[:]
    del need_calibration_set_hot[:]
    del need_calibration_set[:]
    del time_point[:]

    write_pnt_data(header,header_list,res_data,path_to_calib,filename)








