#!/usr/bin/python
import json
import subprocess
import os
import sys
from scipy.interpolate import interp1d
import shutil
from time import gmtime, strftime
from datetime import datetime, timedelta

input_path = "/opt/OctoPrintScripts/OctoLapse-Data-Overlay/data.json"

input_file = sys.argv[6]
output_file = '/tmp/output.jpg'

col_1 = 60
col_2 = 123

def main():
    ## Open data file
    #################
    file = open(input_path, "r")
    data = json.loads(file.read())

    command = "convert " + input_file 

    # Add Rectangle
    command += " -fill '#0008' -draw 'rectangle 5,980,500,1075'"

    # Progress Bar - Outline
    command += " -fill none -stroke white -strokewidth 1 -draw 'rectangle 10,985, 415 1005'" 
    
    # progress bar fill
    prog_range = [0, 100];
    rect_range = [10, 415];
    interp_prog = interp1d(prog_range, rect_range)
    raw_progress = data['progress']['progress']
    progress = interp_prog(raw_progress)

    command += " -fill white -draw 'rectangle 10, 985, "+str(progress)+", 1005'"
    command += " -fill white -pointsize 16 -annotate +420+1000 '"+str(round(raw_progress,1))+"%'"

    # Add filename
    #command += " -fill white -pointsize 16 -annotate +10+1000 'Filename: '"
    #command += " -fill white -pointsize 16 -annotate +85+1000 '"+data['print_file']['name']+"'"

    # Add Temperature Grid - Right, top, left, bottom
    command += " -fill white -draw 'line 10, 1030, 160, 1030'"  # Horiz Line
    command += " -fill white -draw 'line "+str(col_1)+", 1010, "+str(col_1)+", 1075'" # Vert 1
    command += " -fill white -draw 'line "+str(col_2)+", 1010, "+str(col_2)+", 1075'" # vert 2
    command += " -fill white -pointsize 14 -annotate +10+1023 'Temps'"
    command += " -fill white -pointsize 14 -annotate +10+1047 'Target: '"
    command += " -fill white -pointsize 14 -annotate +10+1067 'Actual: '"
    command += " -fill white -pointsize 14 -annotate +"+str(col_1 + 5)+"+1023 'Hot End'"
    command += " -fill white -pointsize 14 -annotate +"+str(col_2 + 5)+"+1023 'Bed'"

    # Add Temperature Texts:
    command += " -fill white -pointsize 14 -annotate +"+str(col_1 + 5)+"+1047 '"+str(data['he_temp']['target'])+"'"
    command += " -fill white -pointsize 14 -annotate +"+str(col_1 + 5)+"+1067 '"+str(data['he_temp']['actual'])+"'"
    command += " -fill white -pointsize 14 -annotate +"+str(col_2 + 5)+"+1047 '"+str(data['bed_temp']['target'])+"'"
    command += " -fill white -pointsize 14 -annotate +"+str(col_2 + 5)+"+1067 '"+str(data['bed_temp']['actual'])+"'"

    # Add Times
    localtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    
    elap_secs = timedelta(seconds = data['progress']['print_time'])
    elap_time = str(elap_secs)
    #elap_time = strftime("%d %H:%M:%S", data['progress']['print_time'])

    remain_secs = timedelta(seconds = data['progress']['print_time_left'])
    remain_time = str(remain_secs)
    #remain_time = strftime("%d %H:%M:%S", data['progress']['print_time_left'])
    command += " -fill white -pointsize 14 -annotate +205+1023 'Local Time: '"
    command += " -fill white -pointsize 14 -annotate +285+1023 '"+localtime+"'"
    command += " -fill white -pointsize 14 -annotate +189+1045 'Elapsed Time: '"
    command += " -fill white -pointsize 14 -annotate +285+1045 '"+elap_time+"'"
    command += " -fill white -pointsize 14 -annotate +170+1067 'Remaining Time: '"
    command += " -fill white -pointsize 14 -annotate +285+1067 '"+remain_time+"'"



    # Complete Commmand 
    command += " "+output_file
    os.system(command)

    os.system("mv "+output_file+" "+input_file)
    ## Overlay Text
    #subprocess.call(['convert', 'test.jpg',
    #    "-fill '#0008' -draw rectangle 5,980,1910,1075",
    #    "-fill white -pointsize 10 -annotate +10+990 'foobar'",
#
#        'output.jpg'
#    ])


main()
