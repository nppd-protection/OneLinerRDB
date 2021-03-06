#! /usr/bin/env python
#  -*- coding: utf-8 -*-
'''ds_relay_list.py

Open a relay export (.rat) file from Aspen Oneliner v14.5+, look for distance
relay model information, and export model information to a csv.

'''

import sys
import csv
import argparse

_hdr_str = 'NAME; METHOD; ALLOW_GROUND; ALLOW_PHASE; Z2_SUPV; MEMORY; PLZ;' \
           'NPARAMS;'
for n in range(1, 36):
    _hdr_str += ' PINDEX{0}; PLABEL{0}; PDEFAULT{0};'.format(n)

rat_headers = [s.strip() for s in _hdr_str.split(';')[:-1]]


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

    relay_list = []
    with open(args.RAT_FILE, 'r') as f:
        # Read lines until header line for database linkage is found

        l = f.readline()
        while l:
            if l == 'DS RELAY TYPE\n':
                data = []
                while len(l) > 1:
                    l = f.readline()
                    data.extend(l.split(';')[:-1])  # line terminated with ';'
                relay_list.append(data)
            l = f.readline()

    with open(args.CSV_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(rat_headers)
        writer.writerows(relay_list)


if __name__ =='__main__':
    sys.exit(main())