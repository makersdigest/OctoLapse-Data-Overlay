#!/usr/bin/python
import json
import subprocess
import os
import sys
from scipy.interpolate import interp1d
import shutil

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
    command += " -fill '#0008' -draw 'rectangle 5,980,1910,1075'"

    # Progress Bar - Outline
    command += " -fill none -stroke white -strokewidth 1 -draw 'rectangle 10,985, 300, 1005'" 
    
    # progress bar fill
    prog_range = [0, 100];
    rect_range = [10, 300];
    interp_prog = interp1d(prog_range, rect_range)
    raw_progress = data['progress']['progress']
    progress = interp_prog(raw_progress)

    command += " -fill white -draw 'rectangle 10, 985, "+str(progress)+", 1005'"
    command += " -fill white -pointsize 16 -annotate +305+1000 '"+str(round(raw_progress,1))+"%'"
    # Add filename
    #command += " -fill white -pointsize 16 -annotate +10+1000 'Filename: '"
    #command += " -fill white -pointsize 16 -annotate +85+1000 '"+data['print_file']['name']+"'"

    # Add Temperature Grid - Right, top, left, bottom
    command += " -fill white -draw 'line 10, 1030, 200, 1030'"  # Horiz Line
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
