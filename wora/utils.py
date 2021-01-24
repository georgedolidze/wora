import csv
import datetime
from functools import reduce

def duration(start, end):
    mins = (
        datetime.datetime.fromisoformat(end)
        - datetime.datetime.fromisoformat(start)
    ).total_seconds() / 60
    return '{0:02.0f}:{1:02.0f}'.format(mins // 60, mins % 60)

def flatten_list(items):
    if not items:
        return ''
    return reduce(lambda x, y: x + ' ;; ' + y, items)

def out_row(out, fields):
    vals = []
    for key in fields:
        if key not in out.keys():
            vals += [None]
        elif isinstance(out[key], list):
            vals += [flatten_list(out[key])]
        else:
            vals += [out[key]]
    return vals

def _out_dur(out):
    out['duration'] = duration(out['start'], out['end'])
    return out

def writecsv(file, fields, outs):
    writer = csv.writer(file, quoting=csv.QUOTE_ALL)
    writer.writerow(fields)
    list(map(
        writer.writerow,
        map(
            lambda x: out_row(x, fields),
            map(_out_dur, outs)
        )
    ))
