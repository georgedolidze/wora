import sys
import csv
import json

from .utils import *

_FIELDS = [
    'category',
    'issue',
    'scope',
    'start',
    'end',
    'duration',
    'diversity',
    'connectivity',
    'vendors_involved',
    'rfo_category',
    'rfo_description'
]

def master_csv(filename_out, current_date):
    jin = open(filename_out)
    outs = json.load(jin)
    jin.close()

    master_filename = current_date + '-master.csv'
    master = open(master_filename, 'w')
    writecsv(master, _FIELDS, outs)

#if __name__ == '__main__':
#    main()
