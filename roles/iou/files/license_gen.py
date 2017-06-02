#!/usr/bin/python

print "*********************************************************************"
print "Cisco IOU License Generator - Kal 2011, python port of 2006 C version"
print "*********************************************************************"

import os
import socket
import hashlib
import struct

# get the host id and host name to calculate the hostkey
hostid = os.popen("hostid").read().strip()
hostname = socket.gethostname()
ioukey=int(hostid,16)

license_file = os.environ['HOME'] + '/.iourc'
iourc = open(license_file, 'w')

for x in hostname:
    ioukey = ioukey + ord(x)
    #print "hostid=" + hostid +", hostname="+ hostname + ", ioukey=" + hex(ioukey)[2:]
    # create the license using md5sum
    iouPad1 = '\x4B\x58\x21\x81\x56\x7B\x0D\xF3\x21\x43\x9B\x7E\xAC\x1D\xE6\x8A'
    iouPad2 = '\x80' + 39*'\0'
    md5input = iouPad1 + iouPad2 + struct.pack('!i', ioukey) + iouPad1
    iouLicense = hashlib.md5(md5input).hexdigest()[:16]

iourc.write('[license]\n')
iourc.write(hostname + ' = ' + iouLicense + ';\n')

