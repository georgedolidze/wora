import csv
from utils import *

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
    'Environmental', # Including these since they don't need to participate in non-sla list
    'CENIC Internal' # ^

]

def eligibility_function(vendor, lower_duration, upper_duration):
    with open('2020-10-14-credits.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0: # This 'if' allows to skip the first line/header in the csv
                line_count += 1
            else:
                if ((row[0] == vendor) and (hms_to_m(row[5]) >= lower_duration) and (hms_to_m(row[5]) <= upper_duration)):
                    print("{}: Duration is over {} minutes ({})".format(row[1], lower_duration, row[5]))
                #else: 
                #    print("Outage-that-doesn't-meet-SLA-here")

def hms_to_m(s): # For converting the H:M:S duration format to seconds/minutes
    t = 0
    for u in s.split(':'):
        t = 60 * t + int(u)
    return t

def non_sla(HAS_SLA):
    with open('2020-10-14-credits.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0: # This 'if' allows to skip the first line/header in the csv
                line_count += 1
            else:
                if (row[0] not in HAS_SLA):
                    print("{} - {} - Duration: {}".format(row[1], row[0], row[5]))
                    

print("\n\n\nEligible outages per Vendor SLAs\n\n\n")

print("\n\nCenturyLink\n"+"-"*30)
print("> 8-10hrs")
print("\n")
print("> 10-16hrs")
print("\n")
print("> 16+hrs\n")

print("\n\nCharter/TWC/Spectrum\n"+"-"*30)
print("> 4-8hrs")
eligibility_function("Spectrum", 240, 480)
print("")
print("> 8+hrs")
eligibility_function("Spectrum", 480, 99999)
print("")

print("\n\nVerizon/Frontier\n"+"-"*30)
print("> 216+ minutes")
eligibility_function("Frontier", 216, 99999)
print("\n")

print("\n\nComcast\n"+"-"*30)
print("> 40+ minutes")
eligibility_function("Comcast", 40, 99999)
print("\n")

print("\n\nZayo\n"+"-"*30)
print("> 4+ hrs")
eligibility_function("Zayo", 240, 99999)
print("\n")

print("\n\nCVIN/Vast\n"+"-"*30)
print("> 4+ hrs")
eligibility_function("Vast", 240, 99999)
print("\n")

print("\n\nPlumas-Sierra Telecom\n"+"-"*30)
print("> 15+ minutes")
eligibility_function("Plumas-Sierra Telecom", 15, 99999)
print("\n")

print("\n\nCBC/Digital 395\n"+"-"*30)
print("> 15+ minutes")
eligibility_function("CBC", 15, 99999)
print("\n")

print("\n\nGeoLinks\n"+"-"*30)
print("> 4+ hours")
eligibility_function("GeoLinks", 240, 99999)
print("\n")

print("\n\nSouthern California Edison\n"+"-"*30)
print("> 4+ hours")
eligibility_function("SCE", 240, 99999)
print("\n")

print("\n\nWave Broadband\n"+"-"*30)
print("> 1+ minutes")
eligibility_function("WaveBroadband", 1, 99999)
print("\n")

print("\n\nVendors with no SLA\n"+"-"*30)
non_sla(HAS_SLA)