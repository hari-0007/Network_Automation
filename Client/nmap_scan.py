#!/usr/bin/env python3
# Import the modules - mysqlconnector,datetime and OS modules

# Python code to demonstrate the use of 'sys' module
# for command line arguments

import sys
import mysql.connector
import os
from mysql.connector import Error
import datetime

# Function declaration :

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

# function to insert the binary data into the database


def insertBLOB(nmap_id, nmap_data):
    print("Inserting BLOB into Nmap_db_table")
    dt =datetime.datetime.now().date()
    try:
        connection = mysql.connector.connect(host=ipaddr,
                                             database='tshark_db',
                                             user='mysqltest',
                                             password='Pa$$w0rd')

        cursor = connection.cursor()
        sql_insert_blob_query = """ INSERT INTO nmap_loc1
                          (nmap_Id,nmap_data,Date) VALUES (%s,%s,%s)"""

        nmap_file = convertToBinaryData(nmap_data)

        # Convert data into tuple format
        insert_blob_tuple = (nmap_id, nmap_file,dt)
        print("inserting blob_tuple")
        result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
        connection.commit()
        print("Nmap captured data is inserted successfully as a BLOB into nmap_table", result)

    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))

    finally:

         if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

# Variable declaration and assigning with values:

dt_time  = datetime.datetime.now()
nmap_no   = int(dt_time.strftime("%Y%m%d%H%M"))
ipaddr   = '167.71.236.9' # Digital Ocean IP Address%
hostid = sys.argv[1]
#print(ipaddr)
# Main Program
os.system("echo Tshark is going to capture the data")
pwd = os.getcwd()
filepcap = "touch nmap_%s.txt" % (nmap_no)
fileperm = "chmod o=rw nmap_%s.txt" % (nmap_no)
#cmd1 = "sudo tshark -i %s -c %s -w %s/capture_%s.pcap" % (sel_dev, cap_time, pwd, cap_no)
cmd1 = " sudo nmap %s -oN %s/nmap_%s.txt"%(hostid,pwd,nmap_no)
os.system(filepcap)
os.system(fileperm)
os.system(cmd1)

db = mysql.connector.connect(host=ipaddr, database='tshark_db', user='mysqltest', password='Pa$$w0rd')
cursor = db.cursor()

cmd2 = "%s/nmap_%s.txt" % (pwd, nmap_no)
print(cmd2)

insertBLOB(nmap_no, cmd2)



filePath = "%s"%(cmd2)
os.system("rm "+ filePath)
