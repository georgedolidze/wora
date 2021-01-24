from .jira import JiraWrapper

def supplement_jira_fields(outages):
    jira = JiraWrapper()
    outs = []
    for out in outages:
        out['vendors_involved'] = jira.vendors_involved(out['issue'])
        out['telco_ticket_id'] = jira.get_issue_field(
            out['issue'], 'Telco Ticket ID'
        )
        outs += [out]
    return outs
