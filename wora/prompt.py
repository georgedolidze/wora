import os
import sys
import json
import datetime

from bullet import Bullet, Input, YesNo

from .constants import IMPACT_CATEGORIES

RFO_CATEGORIES = [
    'unknown',
    'provider maintenance',
    'faulty line card',
    'faulty optic',
    'fiber cut',
    'fiber damage',
    'CPE reset',
    'higher level carrier',
    'other'
]

RFO_CATEGORIES_ENV = [
    'utility maintenance',
    'power outage',
    'wildfire',
    'earthquake'
]

TELCOS = [
    'CENIC Internal',
    'Frontier',
    'AT&T',
    'WilTel',
    'CenturyLink (Level3)',
    'Sunesys',
    'Comcast',
    'Cogent',
    'Zayo',
    'Vast',
    'WaveBroadband',
    'CBC',
    'Cal-Ore',
    'Cox',
    'Crown Castle',
    'GeoLinks',
    'Hunter Communications',
    'Plumas-Sierra Telecom',
    'Spectrum',
    'SuddenLink',
    'Wilcon',
    'SCE',
    'Environmental'
]


def prompt(current_date):
    filename = current_date + '-email-blob.json'
    filename_out = current_date + '-finalized-blob.json'
    jin = open(filename)
    outs = json.load(jin)
    jin.close()
    jout = open(filename_out, 'w')
    news = []
    for out in outs:
        _=os.system('clear')
        print('Summary of the outage:\n')
        print(json.dumps(out, indent=4))
        print('\nhttps://servicedesk.cenic.org/browse/' + out['issue'] + '\n')
        out['category'] = Bullet(
            prompt='What category do the impacted sites fall under?',
            choices=IMPACT_CATEGORIES
        ).launch()
        print('')
        out['rfo_category'] = Bullet(
            prompt='What category does the reason for the outage fall under?',
            choices=(RFO_CATEGORIES + RFO_CATEGORIES_ENV)
        ).launch()
        sys.stdout.write('\nDescribe the reason for the outage further, if necessary: ')
        add = input()
        out['rfo_description'] = add.strip()
        if add:
            print('')
        else:
            print('\n')
        while not out['telco_ticket_id']:
            sys.stdout.write('\nEnter telco ticket numbers, separated by commas if multiple: ')
            add = input()
            out['telco_ticket_id'] = add.strip()
            print('\n')
        if out['rfo_category'] in RFO_CATEGORIES_ENV:
            out['vendors_involved'] = ['Environmental']
        if not out['vendors_involved']:
            out['vendors_involved'] = [Bullet(
                prompt='What provider is associated with the outage?',
                choices=TELCOS
            ).launch()]
            print('')
        news += [out]
    jout.write(json.dumps(news, indent=4))

    return filename_out


#if __name__ == '__main__':
#    main()

