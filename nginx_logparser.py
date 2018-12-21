#!/usr/bin/python
# Nginx access.log parser
#
# Input:
#   - Nginx log file name/path
# Output:
#   - Count of HTTP codes
#   - Group by IP address
#   - Sort by ascending (TBD)
# Usage:
#   - python nginx_logparser.py -log access.log -f general << Sort and count all status codes
#   - python nginx_logparser.py -log access.log -f error << Sort and count all codes except 2xx/3xx

import sys
import re
import argparse
from pprint import pprint
from collections import Counter
from itertools import groupby

# Regex strings for nginx log
generalformat = re.compile(r"""(?P<ipaddress>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(?P<dateandtime>\d{2}\/[a-z]{3}\/\d{4}:\d{2}:\d{2}:\d{2} (\+|\-)\d{4})\] ((\"(GET|POST) )(?P<url>.+)(http\/1\.1")) (?P<statuscode>\d{3}) (?P<bytessent>\d+) (["](?P<refferer>(\-)|(.+))["]) (["](?P<useragent>.+)["])""", re.IGNORECASE)
errorformat = re.compile(r"""(?P<ipaddress>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(?P<dateandtime>\d{2}\/[a-z]{3}\/\d{4}:\d{2}:\d{2}:\d{2} (\+|\-)\d{4})\] ((\"(GET|POST) )(?P<url>.+)(http\/1\.1")) (?P<statuscode>(4[0-9]{2}|5[0-8][0-9]|59[0-9])) (?P<bytessent>\d+) (["](?P<refferer>(\-)|(.+))["]) (["](?P<useragent>.+)["])""", re.IGNORECASE)

# Needed keys to work with
keys = ['ipaddress', 'statuscode']

def parse_log(logfile, regex, keys):
    """
    Parser fucntion
    logfile - nginx access log argument
    regex - nginx log string regex
    keys - keys list to sort
    """
    data_dict = dict()
    data_list = list()
    datafile = open(logfile, 'r')
    for l in datafile.readlines():
        data = re.search(regex, l)
        #Create new dict from groupdict with only needed values
        try:
            data_dict = {x:data.groupdict()[x] for x in keys}
        except AttributeError:
            continue
        #Append each dict as list elements to store all repeated value pairs
        data_list.append(data_dict)
    datafile.close()
    return data_list

def group_log(log_list, name, count):
    """
    Group function
    log_list - list with parsed nginx log keys/values
    name - field name to group by
    count - field name to count
    """
    f = lambda x: x[name]
    group_dict = {k: Counter(d[count] for d in g) for k, g in groupby(log_list, f)}
    return group_dict


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Nginx logparser')
    parser.add_argument('-log', action="store", dest="log", required=True)
    parser.add_argument('-f', action="store", dest="filter", required=True)
    args = parser.parse_args()
    if args.log and args.filter is not None:
        if args.filter == 'general':
            print('Parsing log file - ' + args.log)
            print(' ')
            pprint(group_log(parse_log(args.log, generalformat, keys),'ipaddress','statuscode'))
        elif args.filter == 'error':
            print('Parsing log file - ' + args.log)
            print(' ')
            pprint(group_log(parse_log(args.log, errorformat, keys),'ipaddress','statuscode'))
        else:
            print('Wrong format, please use "general" or "error" filter.')
            sys.exit()

