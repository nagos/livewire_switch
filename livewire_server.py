#!/usr/bin/env python

import SocketServer
import select
from struct import unpack, pack
import json
from LWRPClient import LWRPClient
import AxiaLivewireAddressHelper

handshake = "PERP\x00\x01\x00\x00"
conf_ip = ""
conf_dst = 0
conf_src = []

def get_livewire():
    LWRP = LWRPClient(conf_ip, 93)
    LWRP.login()
    
    dst_data = LWRP.destinationData()
    src = dst_data[conf_dst-1]['attributes']['address']

    LWRP.stop()

    return src

def switch_livewire(index):
    LWRP = LWRPClient(conf_ip, 93)
    LWRP.login()
    
    print "Send setDestination"
    LWMulticastNumber = AxiaLivewireAddressHelper.streamNumToMulticastAddr(conf_src[index])
    LWRP.setDestination(conf_dst, LWMulticastNumber)
    LWRP.stop()

def send_leds(socket):
    src = get_livewire()
    for i in range(len(conf_src)):
        LWMulticastNumber = AxiaLivewireAddressHelper.streamNumToMulticastAddr(conf_src[i])
        if(src == LWMulticastNumber):
            send_led(socket, i+1, 1)
        else:
            send_led(socket, i+1, 0)


def send_led(socket, n, value):
    try:
        socket.sendall(pack('>IxBHBH', 11, 2, n, 1, value))
    except:
        pass

def parse_message(socket, data):
    (msg_size, msg_type, type_specific, data_type, data) = unpack('>IxBHBH', data)
    if(msg_type == 0):
        print "keepalive"
        socket.sendall(pack('>IxBHBH', 11, 1, 0, 1, 0))
    elif(msg_type == 2):
        if(data==0):
            print "set", type_specific, data
            switch_livewire(type_specific-1)

class MyTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        self.request.sendall(handshake)
        self.request.recv(len(handshake))
        for i in range(1, 6):
            send_led(self.request, i, 0)
        while True:
            try:
                ready = select.select([self.request], [], [], 1)
                if ready:
                    data = self.request.recv(11)
                    if not data:
                        break
                    parse_message(self.request, data)
                send_leds(self.request)
            except:
                break

if __name__ == "__main__":
    with open('config.json') as json_file:
        data = json.load(json_file)
        conf_ip = data['DeviceIP']
        conf_dst = data['DeviceOutputNum']
        for i in range(min(5, len(data['Sources']))):
            conf_src.append(int(data['Sources'][i]['SourceNum']))

    SocketServer.TCPServer.allow_reuse_address = True
    server = SocketServer.TCPServer(("", 10010), MyTCPHandler)
    server.serve_forever()
