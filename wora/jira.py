import logging

from jira import JIRA
from jira.exceptions import JIRAError

from .login import get_auth, save_auth

_DEFAULT_URL = 'https://servicedesk.cenic.org'

class JiraWrapper():
    _field_lookup = None

    def __init__(self, force_login=False, url=_DEFAULT_URL):
        auth = get_auth('JIRA', force=force_login)
        self.session = JIRA(url, basic_auth=auth)
        save_auth('JIRA', auth)

    def _init_field_lookup(self, force=False):
        if self._field_lookup is None or force:
            self._field_lookup = {}
            for field in self.session.fields():
                self._field_lookup[field['name']] = field['id']

    def field_id(self, name):
        if self._field_lookup is None:
            self._init_field_lookup()
        return self._field_lookup[name]

    def get_issue_field(self, issue, field):
        try:
            return getattr(
                self.session.issue(issue).fields(),
                self.field_id(field)
            )
        except JIRAError as err:
            logging.warning('%s', err)
            return None

    def vendors_involved(self, issue):
        vendors = self.get_issue_field(issue, 'Vendors involved')
        if vendors is None:
            return []
        return list(map(
            lambda x: x.value,
            vendors
        ))
