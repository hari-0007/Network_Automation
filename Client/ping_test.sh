#!/bin/bash
SERVERIP=10.8.0.1

ping -c 3 $SERVERIP > /dev/null 2>&1
if [ $? -ne 0 ]
then
   # restart the service
   sudo service openvpn restart
fi
  echo "VPN is connected"
