import mysql.connector
import socket
import array
import struct
import fcntl
import datetime
import time

def get_local_interfaces():
    """ Returns a dictionary of name:ip key value pairs. """
    MAX_BYTES = 4096
    FILL_CHAR = b'\0'
    SIOCGIFCONF = 0x8912
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    names = array.array('B', MAX_BYTES * FILL_CHAR)
    names_address, names_length = names.buffer_info()
    mutable_byte_buffer = struct.pack('iL', MAX_BYTES, names_address)
    mutated_byte_buffer = fcntl.ioctl(sock.fileno(), SIOCGIFCONF, mutable_byte_buffer)
    max_bytes_out, names_address_out = struct.unpack('iL', mutated_byte_buffer)
    namestr = names.tobytes()
    namestr[:max_bytes_out]
    bytes_out = namestr[:max_bytes_out]
    ip_dict = {}
    for i in range(0, max_bytes_out, 40):
        name = namestr[ i: i+16 ].split(FILL_CHAR, 1)[0]
        name = name.decode('utf-8')
        ip_bytes   = namestr[i+20:i+24]
        full_addr = []
        for netaddr in ip_bytes:
            if isinstance(netaddr, int):
                full_addr.append(str(netaddr))
            elif isinstance(netaddr, str):
                full_addr.append(str(ord(netaddr)))
        ip_dict[name] = '.'.join(full_addr)

    return ip_dict

connection = mysql.connector.connect(host='167.71.236.9',database='tshark_db',user='mysqltest',password='Pa$$w0rd')
print('Successfully connected to database')
cursor = connection.cursor()

if __name__ == "__main__":
    for iface, ip in get_local_interfaces().items():
        #print("{ip:15s} {iface}".format(ip=ip, iface=iface))
        print(ip)
        #int_ip=ip.format(ip=ip)
        #dt_time  = datetime.datetime.now()
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
       # print(timestamp)
        query4="INSERT INTO nmap_loc1_int (Nmap_date,int_name,IPV4Addr) VALUES ('%s','%s',INET_ATON('%s'));"%(timestamp,iface,ip)
        print(query4)
        cursor.execute(query4)

connection.commit()
cursor.close()
connection.close()
