#!/usr/bin/env python3
# Import the modules - mysqlconnector,datetime and OS modules

import os
import datetime



# Variable declaration and assigning with values:
sel_dev  = 'wlan0'
dt_time  = datetime.datetime.now()
cap_no   = int(dt_time.strftime("%Y%m%d%H%M"))
cap_time = '60'
month=dt_time.strftime("%B")
day=int(dt_time.strftime("%d"))

# Main Program
os.system("echo Tshark is going to capture the data")
pwd = os.getcwd()
filepcap = "touch capture_%s.pcap" % (cap_no)
fileperm = "chmod o=rw capture_%s.pcap" % (cap_no)
cmd1 = "sudo tshark -i %s -c %s -w %s/capture_%s.pcap" % (sel_dev, cap_time, pwd, cap_no)

os.system(filepcap)
os.system(fileperm)
os.system(cmd1)


cmd2 = "%s/capture_%s.pcap" % (pwd, cap_no)
cmd4 = "%s/capture_%s.xml" % (pwd, cap_no)
print(cmd2)

pwd = os.getcwd()
filePath = "%s"%(cmd2)
serverPath = "/home/ramkumar/tshark_output/%s/%d"%(month,day)

#os.system("scp "+filePath+" ramkumar@167.71.236.9:"+serverPath)
cmd3="tshark -r %s -T pdml > %s"%(cmd2,cmd4)
os.system(cmd3)



