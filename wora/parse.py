import re
import logging
import datetime

class ParseError(Exception):
    pass

def parse_date(field, year=None):
    if '(' in field:
        field = field.split('(')[0]
    field = field.strip()
    if year is not None and field.count('/') == 1:
        field += '/' + year
    return datetime.datetime.strptime(field, '%H:%M %Z, %a %m/%d/%Y')

def parse_loss(msg, pattern, fin):
    """
    Search for a regex and return trailing lines until a blank line

    Keyword arguments:
    msg -- message to parse
    pattern -- regular expression to search for
    """
    out = []
    loss_search = pattern.search(msg)
    if loss_search is None:
        return out
    for line in msg[loss_search.end() + 1:].split('\n'):
        if line.strip() == '' or fin.search(line):
            break
        out.append(line.strip())
    return out

def parse_part(msg, pattern):
    """Grab a field pattern from the message, or warn and return empty"""
    match = pattern.search(msg)
    if match is not None:
        return match.groups()[-1].strip().replace('\n', '')
    raise ParseError('Missing field')

def parse_issue(subj, pattern_primary, pattern_secondary):
    match = pattern_primary.search(subj)
    if match is None:
        match = pattern_secondary.search(subj)
        if match is None:
            raise ParseError('Could not understand the dang subject line')
        return match.group(1)
    return 'NOC-' + match.group(1)

class Parser():
    def __init__(self):
        self.patterns = {
            'issue_old': re.compile(r'\[CENIC\s+#(\d+)\].*'),
            'issue_new': re.compile(r'\[CENIC\s+(NOC\-\d+)\].*'),
            'resolved': re.compile(r'^(Summary of RESOLVED outage:)', re.MULTILINE),
            'scope': re.compile(r'(SCOPE:)\s+(.*\n|.*\n.*)\n', re.MULTILINE),
            'start': re.compile(r'(START:)\s+(.*)'),
            'end': re.compile(r'(END:)\s+(.*)'),
            'diversity': re.compile(
                r'^(LOSS OF DIVERSITY FOR:)\s*$',
                re.MULTILINE
            ),
            'connectivity': re.compile(
                r'^(LOSS OF CONNECTIVITY FOR:)\s*$',
                re.MULTILINE
            ),
            'fin': re.compile(r"""(
                COMMENTS:
                |IMPACTED\sXD\sCLRs:
                |IMPACTED\sCLRs:
                |Layer\s\d\scircuits affected:
                |Layer\s\d:
                |LOSS\sOF\sCONNECTIVITY\sFOR:)""", re.VERBOSE)
        }

    def parse(self, msg, subj, year=None):
        """
        Parses an outage announcement and returns dictionary of identified fields

        Searches for scope, start, end, LoD, and LoC fields in the message.

        Args:
        msg -- text to search in
        subj -- subject of message to get issue from
        year -- year to assume for the dates
        """
        subj_line = ' '.join(subj.splitlines())
        start = None
        end = None
        try:
            start = parse_date(parse_part(msg, self.patterns['start']), year)
        except ValueError as err:
            logging.warning('%s: could not parse start: %s', subj_line, err)
        try:
            end = parse_date(parse_part(msg, self.patterns['end']), year)
        except ValueError as err:
            logging.warning('%s: could not parse end: %s', subj_line, err)
        return {
            'issue': parse_issue(subj, self.patterns['issue_old'],
                                 self.patterns['issue_new']),
            'start': start,
            'end': end,
            'scope': parse_part(msg, self.patterns['scope']),
            'diversity': parse_loss(msg, self.patterns['diversity'],
                                    self.patterns['fin']),
            'connectivity': parse_loss(msg, self.patterns['connectivity'],
                                       self.patterns['fin'])
        }

    def is_resolved_outage(self, msg):
        return self.patterns['resolved'].search(msg) is not None
