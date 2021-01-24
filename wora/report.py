import sys
import json

from .utils import *
from .constants import IMPACT_CATEGORIES

def _txt(out):
    sep = '\n    '
    return ''.join([
        'ISSUE: ', out['issue'], sep,
        'SCOPE: ', out['scope'], sep,
        'START: ', out['start'], sep,
        'END: ', out['end'], sep,
        #'DURATION: ', utils.duration(out['start'], out['end']), sep,
        #'DIVERSITY: ', utils.flatten_list(out['diversity']), sep,
        #'CONNECTIVITY: ', utils.flatten_list(out['connectivity']), sep,
        #'PROVIDER: ', utils.flatten_list(out['vendors_involved']), sep,
        'DURATION: ', duration(out['start'], out['end']), sep,
        'DIVERSITY: ', flatten_list(out['diversity']), sep,
        'CONNECTIVITY: ', flatten_list(out['connectivity']), sep,
        'PROVIDER: ', flatten_list(out['vendors_involved']), sep,
        'REASON: ', '[', out['rfo_category'], '] ', out['rfo_description'],
        '\n\n'
    ])

def _iter(outs):
    result = 'Total: {}\n\n'.format(len(outs))
    cat_hier = {}
    for cat in IMPACT_CATEGORIES:
        cat_hier[cat] = []
    for out in outs:
        cat_hier[out['category']] += [out]
    count = 0
    for cat in IMPACT_CATEGORIES:
        count += 1
        result += '{}. {}: {}\n'.format(count, cat, len(cat_hier[cat]))
    result += '\n'
    count = 0
    for cat in IMPACT_CATEGORIES:
        count += 1
        result += str(count) + '. ' + cat + '\n\n'
        for out in cat_hier[cat]:
            result += _txt(out)
        result += '\n'
    return result

def report(filename_out, current_date):
    jin = open(filename_out)
    outs = json.load(jin)
    jin.close()

    report_filename = current_date + '-report.txt'
    txt = open(report_filename, 'w')
    txt.write(_iter(outs))
    txt.close()

#if __name__ == '__main__':
#    main()
