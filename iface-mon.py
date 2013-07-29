#!/usr/bin/env python2.7

import subprocess
from termcolor import colored
import os
from time import sleep
import argparse
import datetime 

def check_iface(value):
    if value:
        if not os.path.isdir("/sys/class/net/%s"%value):
            raise argparse.ArgumentTypeError("Interface %s not found or is down"%value)
        return value
    return None

def get_interfaces():
    return [dir for dir in os.listdir('/sys/class/net/') if os.path.isdir(os.path.join('/sys/class/net', dir))]  

def read_nic_status(nic):
    if os.path.isfile("/sys/class/net/%s/carrier"%nic):
        a = open("/sys/class/net/%s/carrier"%nic)
        status = int(a.read())
        a.close()
        if status == 1:
            return True
    return False

def main():
    op = argparse.ArgumentParser(description="Interface carrier monitoring script. Program is monitoring interfaces using /sys subsystem and returning True for interfaces with carrier plugged on and False for carrier plugged off.", prog="iface_mon")
    op.add_argument('--interval', '-i', help="Interval in seconds between checks (default 1s)", default=1, type=int)
    op.add_argument('--print-date', '-d', help="Print date for every check (default no)", action="store_true", dest="date")
    op.add_argument('--interface', '-I', help="Monitor only this interface. Can be used multiple times (default all interfaces)", type=check_iface, action="append")
    options = op.parse_args()
    interfaces = sorted(get_interfaces())
    if options.interface:
        interfaces = set(options.interface)
    print colored("Folowing %s interfaces are monitored: %s\n---------------------------------------------\n\n"%(len(interfaces), interfaces), 'yellow')
    header = ""
    if options.date:
        header += "\t\t\t\t"
    header += '\t'.join(interfaces)
    print colored(header, 'white')
    while True:
        output_line = ""
        status = list()
        for iface in interfaces:
            status.append(read_nic_status(iface))
        if options.date:
            output_line += "%s\t"%datetime.datetime.now()
        output_line += '\t'.join(colored("%s"%value, 'green') if value is True else colored("%s"%value, 'red') for value in status)
        print output_line
        if options.interval > 0:
            sleep(options.interval)
                    

if __name__ == "__main__":
    main()

