#!/usr/bin/env python

import argparse
from LWRPClient import LWRPClient
import AxiaLivewireAddressHelper
import time

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('ip')
    parser.add_argument('dst', type=int)
    parser.add_argument('src', type=int)
    args = parser.parse_args()

    print "Connecting"
    LWRP = LWRPClient(args.ip, 93)
    LWRP.login()
    
    print "Send setDestination"
    LWMulticastNumber = AxiaLivewireAddressHelper.streamNumToMulticastAddr(args.src)
    LWRP.setDestination(args.dst, LWMulticastNumber)

    print "destinationData"
    print LWRP.destinationData()

    LWRP.stop()
