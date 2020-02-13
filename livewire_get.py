#!/usr/bin/env python

import argparse
from LWRPClient import LWRPClient
import AxiaLivewireAddressHelper
import time

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('ip')
    parser.add_argument('dst', type=int)
    args = parser.parse_args()

    print "Connecting"
    LWRP = LWRPClient(args.ip, 93)
    LWRP.login()
    
    dst_data = LWRP.destinationData()
    print "Source"
    print dst_data[args.dst-1]['attributes']['address']

    LWRP.stop()

