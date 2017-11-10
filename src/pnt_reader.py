import os
import struct
import re

from my_config import nrays

def get_header(filename):

    header = dict()
    header_list = []

    f = open(filename,"r")

    first_line = f.readline()

    header_re = re.compile(r'(?P<key>\w*)\s*(?P<value>.*)')

    res_dict = header_re.search(first_line).groupdict()
    
    header[res_dict["key"]] = res_dict["value"]

    header_list.append(res_dict["key"])

    for k in xrange(int(header["numpar"])-1):
        line = f.readline()
        res_dict = header_re.search(line).groupdict()
        header_list.append(res_dict["key"])
        header[res_dict["key"]] = res_dict["value"]

    f.close()
    return header,header_list

def get_data(filename,header):
    print "reading"
    nbands = int(header["nbands"])
    npoints = int(header["npoints"])
    modulus = [ x for x in xrange(nbands)]
    data = []
    p = 0 
    modulus.append(max(modulus)+1)


    with open(filename, 'rb') as inh:
        for k in xrange(int(header["numpar"])):
            line = inh.readline()

        for t in range(npoints):
            data.append([])
            for r in range(nrays):
                data[t].append([])
                data[t][r].extend(list(struct.unpack('f'*len(modulus),inh.read(4*len(modulus)))[0:(nbands+1)]))                       
    return data

def write_pnt_data(header,header_list,data,path,name):
    print "writing"
    nbands = int(header["nbands"])
    npoints = int(header["npoints"])
    f = open(path+name,"w")
    l = [len(x) for x in header_list]
    max_len = max(l)+1

    for key in header_list:
        f.write(key.ljust(max_len)+header[key]+"\n")
    f.close()
    f = open(path+name,"ab")
    for t in range(npoints):
        for r in range(nrays):
            s = struct.pack('f'*(nbands+1),*data[t][r]) 
            f.write(s) 
    f.close()
