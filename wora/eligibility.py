import csv
from .utils import *

HAS_SLA = [
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
    'Crown Castle',
    'GeoLinks',
    'Plumas-Sierra Telecom',
    'Spectrum',
    'Wilcon',
    'SCE',
    'Charter',
    'Cal-Ore',
    'Southern California Edison',
    'Environmental', # Including these since they don't need to participate in non-sla list
    'CENIC Internal' # ^

]

def eligibility_function(csv_name, vendor, lower_duration, upper_duration):
    with open(csv_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        output = ""
        for row in csv_reader:
            if line_count == 0: # This 'if' allows to skip the first line/header in the csv
                line_count += 1
            else:
                if ((vendor in row[0]) and (row[6] != 'fiber cut') and (row[6] != 'fiber damage') and (hms_to_m(row[5]) >= lower_duration) and (hms_to_m(row[5]) <= upper_duration)):
                    output += "{}: Duration is over {} minutes ({}). \nRFO: {}\nVendor ticket: {}\nStart Time: {}\nEnd Time: {}\n".format(row[1], lower_duration, row[5], row[6], row[2], row[3], row[4]) + "\n"
    return output

def hms_to_m(s): # For converting the H:M:S duration format to seconds/minutes
    t = 0
    for u in s.split(':'):
        t = 60 * t + int(u)
    return t

def non_sla(csv_name, HAS_SLA):
    with open(csv_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        output = ""
        for row in csv_reader:
            if line_count == 0: # This 'if' allows to skip the first line/header in the csv
                line_count += 1
            else:
                if ((';;' not in row[0]) and (row[0] not in HAS_SLA)):
                    output += "{} - {} - Duration: {}. \nRFO: {}".format(row[1], row[0], row[5], row[6]) + '\n\n'
                #print(row[0].split(';;'))
    return output
                    
def eligibility_print(csv_name):

    output = "\n\n\nEligible outages per Vendor SLAs\n\n\n"
    
    output += "\n\nCenturyLink\n"+"-"*30 + "\n"
    output += "> 8-10hrs"  + "\n"
    output += str(eligibility_function(csv_name, "CenturyLink (Level3)", 480, 600))  + "\n"
    output += "\n"  + "\n"
    output += "> 10-16hrs"  + "\n"
    output += str(eligibility_function(csv_name, "CenturyLink (Level3)", 600, 960))  + "\n"
    output += "\n"  + "\n"
    output += "> 16+hrs\n" 
    output += str(eligibility_function(csv_name, "CenturyLink (Level3)", 960, 99999))  + "\n"

    output += "\n\nCharter/TWC/Spectrum\n"+"-"*30 + "\n"
    output += "> 4-8hrs"  + "\n"
    output += str(eligibility_function(csv_name, "Spectrum", 240, 480))  + "\n"
    output +=  ""  + "\n"
    output +=  "> 8+hrs"  + "\n"
    output += str(eligibility_function(csv_name, "Spectrum", 480, 99999))  + "\n"
    output += ""  + "\n"

    output += "\n\nVerizon/Frontier\n"+"-"*30 + "\n"
    output += "> 216+ minutes" + "\n"
    output += str(eligibility_function(csv_name, "Frontier", 216, 99999)) + "\n"
    output += "\n" + "\n"

    output += "\n\nComcast\n"+"-"*30 + "\n"
    output += "> 40+ minutes" + "\n"
    output += str(eligibility_function(csv_name, "Comcast", 40, 99999)) + "\n"
    output += "\n" + "\n"

    output += "\n\nZayo\n"+"-"*30 + "\n"
    output += "> 4+ hrs" + "\n"
    output += str(eligibility_function(csv_name, "Zayo", 240, 99999)) + "\n"
    output += "\n" + "\n"

    output += "\n\nCVIN/Vast\n"+"-"*30 + "\n"
    output += "> 4+ hrs" + "\n"
    output += str(eligibility_function(csv_name, "Vast", 240, 99999)) + "\n"
    output += "\n" + "\n"

    output += "\n\nPlumas-Sierra Telecom\n"+"-"*30 + "\n"
    output += "> 15+ minutes" + "\n"
    output += str(eligibility_function(csv_name, "Plumas-Sierra Telecom", 15, 99999)) + "\n"
    output += "\n" + "\n"

    output += "\n\nCBC/Digital 395\n"+"-"*30 + "\n"
    output += "> 15+ minutes" + "\n"
    output += str(eligibility_function(csv_name, "CBC", 15, 99999)) + "\n"
    output += "\n" + "\n"

    output += "\n\nGeoLinks\n"+"-"*30 + "\n"
    output += "> 4+ hours" + "\n"
    output += str(eligibility_function(csv_name, "GeoLinks", 240, 99999)) + "\n"
    output += "\n" + "\n"

    output += "\n\nSouthern California Edison\n"+"-"*30 + "\n"
    output += "> 4+ hours" + "\n"
    output += str(eligibility_function(csv_name, "SCE", 240, 99999)) + "\n"
    output += "\n" + "\n"

    output += "\n\nWave Broadband\n"+"-"*30 + "\n"
    output += "> 1+ minutes" + "\n"
    output += str(eligibility_function(csv_name, "WaveBroadband", 1, 99999)) + "\n"
    output += "\n" + "\n"

    output += "\n\nCal-Ore\n"+"-"*30 + "\n"
    output += "> 4+ hours" + "\n"
    output += str(eligibility_function(csv_name, "Cal-Ore", 240, 99999)) + "\n"
    output += "\n" + "\n"

    output += "\n\nVendors with no SLA\n"+"-"*30 + "\n"
    output += str(non_sla(csv_name, HAS_SLA)) + "\n"

    return output

def eligibility_report(csv_name, current_date):

    report_filename = current_date + '-eligibility_report.txt'
    txt = open(report_filename, 'w')
    txt.write(eligibility_print(csv_name))
    txt.close()
