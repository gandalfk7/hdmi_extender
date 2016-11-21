#!/usr/bin/python2

#Packet sniffer in python
#For Linux - Sniffs all incoming and outgoing packets :)
#Silver Moon (m00n.silv3r@gmail.com)
#modified by danman


import socket, sys
from struct import *
import struct
import binascii


#Convert a string of 6 characters of ethernet address into a dash separated hex string

def eth_addr (a) :
  b = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (ord(a[0]) , ord(a[1]) , ord(a[2]), ord(a[3]), ord(a[4]) , ord(a[5]))
  return b


#create a AF_PACKET type raw socket (thats basically packet level)
#define ETH_P_ALL    0x0003          /* Every packet (be careful!!!) */
try:
    s = socket.socket( socket.AF_PACKET , socket.SOCK_RAW , socket.ntohs(0x0003))
except socket.error , msg:
    print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#sock.bind(('', 2068))
# wrong: mreq = struct.pack("sl", socket.inet_aton("224.51.105.104"), socket.INADDR_ANY)
mreq = struct.pack("=4sl", socket.inet_aton("226.2.2.2"), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)


sender="000b78006001".decode("hex")
#sender = binascii.a2b_hex("000b78006001")  bc5ff4730e6f
#sender = binascii.a2b_hex("bc5ff4730e6f")
#print binascii.b2a_hex(sender)
notopen=1
# = open('/tmp/fifo', 'w')
print "--myboundary\nContent-Type: image/jpeg\n"

# receive a packet
while True:
    packet = s.recvfrom(65565)

    #packet string from tuple
    packet = packet[0]

    #parse ethernet header
    eth_length = 14

    eth_header = packet[:eth_length]
    eth = unpack('!6s6sH' , eth_header)
    eth_protocol = socket.ntohs(eth[2])


    if (packet[6:12] == sender) & (eth_protocol == 8) :

        #Parse IP header
        #take first 20 characters for the ip header
        ip_header = packet[eth_length:20+eth_length]

        #now unpack them :)
        iph = unpack('!BBHHHBBH4s4s' , ip_header)

        version_ihl = iph[0]
        version = version_ihl >> 4
        ihl = version_ihl & 0xF

        iph_length = ihl * 4

        ttl = iph[5]
        protocol = iph[6]
        s_addr = socket.inet_ntoa(iph[8]);
        d_addr = socket.inet_ntoa(iph[9]);

        #UDP packets
        if protocol == 17 :
            u = iph_length + eth_length
            udph_length = 8
            udp_header = packet[u:u+8]

            #now unpack them :)
            udph = unpack('!HHHH' , udp_header)

            source_port = udph[0]
            dest_port = udph[1]
            length = udph[2]
            checksum = udph[3]

            #get data from the packet
            h_size = eth_length + iph_length + udph_length
            data = packet[h_size:]

            if (dest_port==2068):
              frame_n=ord(data[0])*256+ord(data[1])
              part=ord(data[2])*256+ord(data[3])
              if (part==0) : # & (notopen==1) :
                 #f = open('files/'+str(frame_n)+"_"+str(part).zfill(3)+'.jpg', 'w')
		 #fname = str(frame_n)+"_"+str(part).zfill(3)+'.jpg'
		 #fname = 'file.jpg'
		 print "\n--myboundary\nContent-Type: image/jpeg\n"
                 notopen=0
		 #print 'File ' + str(frame_n) + ' created.'
              if notopen==0:
                 #f.write(data[4:])
		 #print data[4:]
		 sys.stdout.write(data[4:])
		 #with open(fname, 'wb') as fin:
		    #sys.stdout.write(fin.write(data[4:]))
		    #print fin.write(data[4:])
