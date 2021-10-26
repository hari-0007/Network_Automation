#!/bin/sh
SERVICE=service;

if ps ax | grep -v grep | grep $openvpn > /dev/null
then
    echo "$SERVICE service running, everything is fine"
else
    echo "$SERVICE is not running"
    echo "$SERVICE is not running!" | mail -s "$SERVICE down" root
fi
