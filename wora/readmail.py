import logging
import email
import datetime

import easyimap

from .login import get_auth, save_auth
from .parse import Parser, ParseError

CENIC_HOST = 'imap-vip.cenic.org'

def _criterion(start, end):
    return ' '.join([
        'SENTSINCE',
        start.strftime('%d-%b-%Y'),
        'SENTBEFORE',
        end.strftime('%d-%b-%Y')
    ])

def readmail(start, end):
    parser = Parser()
    auth = get_auth('MAIL')
    inbox = easyimap.connect(CENIC_HOST, auth[0], auth[1], 'ops-announce')
    save_auth('MAIL', auth)
    mails = inbox.listup(
        limit=1000,
        criterion=_criterion(start, end)
    )
    outages = []
    for mail in mails:
        maildate = datetime.datetime.fromtimestamp(
            email.utils.mktime_tz(email.utils.parsedate_tz(mail.date))
        )
        if parser.is_resolved_outage(mail.body):
            try:
                entry = parser.parse(
                    mail.body, mail.title, year=str(maildate.year)
                )
            except ParseError:
                logging.error('%s', ' '.join(mail.title.splitlines()))
                continue
            if entry not in outages:
                outages += [entry]
    return outages
