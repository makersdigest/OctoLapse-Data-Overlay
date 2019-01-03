#!/usr/bin/python
import urllib2
import json
import sys

output_file = "/opt/OctoPrintScripts/OctoLapse-Data-Overlay/data.json"

def getRequest(path):
    octoprintUrl = "http://192.168.1.75:5000/api"
    
    fullPath = octoprintUrl + path

    request = urllib2.Request(fullPath, headers = {
        "X-Api-Key": "70D94A02DDD14699ADFB6820ADAEF17F"
    })

    data = urllib2.urlopen(request).read()

    return json.loads(data)
    

def main():

    # Process Job information
    #########################
    job = getRequest("/job")

    # name, size
    print_file = job['job']['file']

    # completion, printTime, printTimeLeft
    progress   = job['progress']

    ## Process Printer Information
    ##############################
    printer = getRequest("/printer")

    # actual, target
    bed = printer['temperature']['bed']
    
    # actual, target
    he  = printer['temperature']['tool0']

    outputData = {
        'print_file': { 'name': print_file['name'], 'size': print_file['size'] },
        'progress': {
            'progress': progress['completion'],
            'print_time': progress['printTime'],
            'print_time_left': progress['printTimeLeft']
        },
        'bed_temp': {'target': bed['target'], 'actual': bed['actual'] },
        'he_temp': {'target': he['target'], 'actual': he['actual']}
    }

    ## Write file
    #############
    file = open(output_file, "w")
    file.write(json.dumps(outputData))
    file.close()








main()



