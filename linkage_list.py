#! /usr/bin/env python
#  -*- coding: utf-8 -*-
'''linkage_list.py

Open a relay export (.rat) file from Aspen Oneliner v14.5+, look for relay 
linkage information, and export relay database linkage information to a csv.

'''

import sys
import csv
import argparse

_hdr_str = 'BUS_NO1; BUS1; KV1; BUS_NO2; BUS2; KV2; CKT; BTYP;' \
           'DEVTYPE; DEVID; LABEL; RDBQUERY; RETSCRIP; STORESCRIPT;'
rat_rdb_headers = [s.strip() for s in _hdr_str.split(';')[:-1]]


def main(argv=None):

    parser = argparse.ArgumentParser()

    parser.add_argument('RAT_FILE',
                        help='OneLiner relay export (.rat) file to be '
                             'processed.')
    parser.add_argument('CSV_FILE',
                        help='Name to output csv file to. Any existing file '
                             'will be overwritten.')

    if argv is None:
        argv = sys.argv
    args = parser.parse_args()

    linkage_list = []
    with open(args.RAT_FILE, 'r') as f:
        # Read lines until header line for database linkage is found

        l = f.readline()
        while l:
            if l == 'RDBX:ASPENRDB\n':
                data = []
                while len(data) < 14:
                    l = f.readline()
                    data.extend(l.split(';')[:-1])  # line terminated with ';'
                linkage_list.append(data)
            l = f.readline()

    with open(args.CSV_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(rat_rdb_headers)
        writer.writerows(linkage_list)


if __name__ =='__main__':
    sys.exit(main())