#!/usr/bin/env python3
# Import the modules - mysqlconnector,datetime and OS modules

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


def insertBLOB(cap_id, tshark_data):
    print("Inserting BLOB into tshark_db_table")
    dt =datetime.datetime.now().date()
    try:
        connection = mysql.connector.connect(host=ipaddr,
                                             database='tshark_db',
                                             user='mysqltest',
                                             password='Pa$$w0rd')

        cursor = connection.cursor()
        sql_insert_blob_query = """ INSERT INTO tshark_db_table
                          (cap_id,tshark_data,Date) VALUES (%s,%s,%s)"""

        tshark_file = convertToBinaryData(tshark_data)

        # Convert data into tuple format
        insert_blob_tuple = (cap_id, tshark_file,dt)
        print("inserting blob_tuple")
        result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
        connection.commit()
        print("Tshark captured data is inserted successfully as a BLOB into tshark_db_table", result)

    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")




# Variable declaration and assigning with values:
sel_dev  = 'eth0'
dt_time  = datetime.datetime.now()
cap_no   = int(dt_time.strftime("%Y%m%d%H%M"))
cap_time = '1000'
ipaddr   = '167.71.236.9' # Digital Ocean IP Address%
# Main Program
os.system("echo Tshark is going to capture the data")
pwd = os.getcwd()
filepcap = "touch capture_%s.pcap" % (cap_no)
fileperm = "chmod o=rw capture_%s.pcap" % (cap_no)
cmd1 = "sudo tshark -i %s -c %s -w %s/capture_%s.pcap" % (sel_dev, cap_time, pwd, cap_no)

os.system(filepcap)
os.system(fileperm)
os.system(cmd1)

db = mysql.connector.connect(host=ipaddr, database='tshark_db', user='mysqltest', password='Pa$$w0rd')
cursor = db.cursor()

cmd2 = "%s/capture_%s.pcap" % (pwd, cap_no)
print(cmd2)

insertBLOB(cap_no, cmd2)



filePath = "%s"%(cmd2)
os.system("rm "+ filePath)

