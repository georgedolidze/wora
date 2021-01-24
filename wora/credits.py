import sys
import csv
import json

from .utils import *

_FIELDS = [
    'vendors_involved',
    'issue',
    'telco_ticket_id',
    'start',
    'end',
    'duration',
    'rfo_category',
    'rfo_description'
]

def credits_csv(filename_out, current_date):
    jin = open(filename_out)
    outs = json.load(jin)
    jin.close()

    credits_filename = current_date + '-credits.csv'
    credits = open(credits_filename, 'w')
    writecsv(credits, _FIELDS, outs)

    return credits_filename

#if __name__ == '__main__':
#    main()
