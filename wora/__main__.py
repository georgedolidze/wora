import sys
import datetime
import json
from .prompt import prompt
from .report import report
from .credits import credits_csv
from .master import master_csv
from .eligibility import eligibility_report

from .readmail import readmail
from .supplement import supplement_jira_fields


def _serialize_datetime(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat(sep=' ')
    return obj


def main():
    start = datetime.datetime.strptime(sys.argv[1], '%Y-%m-%d')
    end = datetime.datetime.strptime(sys.argv[2], '%Y-%m-%d')
    return json.dumps(
        supplement_jira_fields(readmail(start, end)),
        indent=4,
        default=_serialize_datetime
    )


if __name__ == '__main__':

    current_date = str(sys.argv[2])
    filename = current_date + '-email-blob.json'
    file = open(filename,'w')
    print('\nParsing emails...')
    file.write(main())
    file.close()
    print('\nEmails parsed')
    
    finalized_blob = prompt(current_date)

    print('\nCompiling report...')
    report(finalized_blob, current_date)
    print('='*50 + "\nReport completed successfully")

    print('\nCompiling credits.csv...')
    csv_name = credits_csv(finalized_blob, current_date)
    print('='*50 + "\ncredits.csv completed successfully")

    print('\nCompiling master.csv...')
    master_csv(finalized_blob, current_date)
    
    print('='*50 + "\nmaster.csv completed successfully")

    #csv_name = 'test.csv' #For testing purposes

    print('\nCompiling Eligibility Report...')
    eligibility_report(csv_name, current_date)
    print('='*50 + "\nEligiblity report completed successfully")
