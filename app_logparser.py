#!/usr/bin/python

import os
import re
import sys
import gzip
import errno
from sys import argv

def data_parse(array,index1,index2):
    """parsing data function"""
    for line_loop in array:
        if ''.join(crn) in line_loop:
            crn_index.append(array.index(line_loop))
            if crn_index[crn_index.index(array.index(line_loop))] - crn_index[crn_index.index(array.index(line_loop))-1] > interval:
                index1 = crn_index[crn_index.index(array.index(line_loop))]
                index2 = crn_index[crn_index.index(array.index(line_loop))-1]
    if index1 and index2:
        try:
            for j in range(crn_index[0],index2+1):
                write_file.write(array[j] + '\n')
            for k in range(index1-1,crn_index[-1]+1):
                write_file.write(array[k] + '\n')
        except IndexError:
            pass
    else:
        try:
            for i in range(crn_index[0],crn_index[-1]+1):
                write_file.write(array[i] + '\n')
        except IndexError:
            pass

#Input parameters
in_file = argv[1:2]
crn = argv[2:3]

if not in_file:
    print 'No input file.'
    print 'Usage: python app_logparser.py <file> <ID>'
    print 'Example: python app_logparser.py log.txt 849873945'
    sys.exit()
else:
    buf = 100000
    interval = 100000 

if not crn:
    print 'No input ID.'
    print 'Usage: python app_logparser.py <file> <ID>'
    print 'Example: python app_logparser.py log.txt 849873945'
    sys.exit()

#Global variables
out_file = (''.join(in_file)) + '_ID_' + (''.join(crn))
data_file = []
crn_index = []
idx1 = 0
idx2 = 0

if ''.join(in_file).endswith('.gz'):
    try:
        read_file = gzip.open(''.join(in_file), 'rb')
        write_file = open(out_file,'w')
    except IOError, ioe:
        print os.strerror(ioe.errno)
        sys.exit()
else:
    try:
        read_file = open(''.join(in_file), 'r')
        write_file = open(out_file,'w')
    except IOError, ioe:
        print os.strerror(ioe.errno)
        sys.exit()

try:
    for line in read_file:
        data_file.append(line.strip('\n'))
        if len(data_file) == buf:
            data_parse(data_file,idx1,idx2)
            data_file = []
            crn_index = []
            idx1 = 0
            idx2 = 0
    data_parse(data_file,idx1,idx2)

finally:
    read_file.close()
    write_file.close()
    if os.stat(out_file).st_size == 0:
        print 'No such ID found.'
        os.remove(out_file)
    else:
        print 'ID filtered.'
    print 'Parsing completed.'
