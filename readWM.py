# This Script is intended to read a WM file and output all empty values of specified fields
# 16.01.2018
# Robert Eber
#
# Reads Input files from same folder as *.WMI
# Outputs in ./imported/Leerwerte_*
# Read files are saved in ./imported.imp and are not read again

import datetime
import os
import sys

debug = 0

# Actual date
now = datetime.datetime.now()

# List of read files
history = open('imported.imp','r')
historyfiles = []
line = 'x'
while line:
    line = history.readline()
    line = line[0:len(line)-1]
    historyfiles.append(line)
history.close()
del historyfiles[len(historyfiles)-1]
historyfiles.append('files.txt')
if debug == 1:
    print(historyfiles)

filenames = []
numberoffiles = 0
for file in os.listdir("."):
    if file.endswith(".WMI"):
        tempfile = file
        if tempfile not in historyfiles:
            print(file)
            filenames.append(tempfile)
            numberoffiles += 1
            
# No file found

if numberoffiles == 0:
    print('No file found.')
    sys.exit(0)

    
# List of WM fields to be extracted with empty values
# GDlist = ['GD504A','GD540B','GD504C','GD504D','GD504E','GD504F','GD504G','GD504H','GD504I','GD504J','GD504K','GD504L','GD504M','GD504N','GD504O','GD504P','GD504Q','GD504R','GD504S','GD504T','GD505J','GD505H']

# List of fields currently relevant
GDlist = ['GD504K','GD504E','GD504J']

for filename in filenames:
    # print (filename)
    # Import file
    #filename = 'AIF_' + now.strftime('%Y%m%d') + '.txt'
    #file = open(filename,'r', encoding='latin1')
    file = open(filename,'r')

    # Output file
    outputfile = 'imported/Leerwerte_' + filename
    extract = open(outputfile,'w')
    
    # Routine
    
    line = file.readline()
    counter = 0
    entries = 0
    print('Read WMfile ' + filename)
    while line:
        counter +=1
        line = file.readline()
        line = line[0:len(line)-1]
        #line = line.split('\n')
        buffer = line.split('\"')
        #print(buffer)
        #break
        BID = buffer[0]
        for element in buffer:
            field = element.split(' ')
            if any(x in field[0] for x in GDlist):
                if element.find('  ') >= 0:
                    #print(BID, element, '\n')
                    extract.write(BID[1:13] + ' ' + element[0:len(element)-1]+ 'TOBEDELETED\n')
                    entries += 1
                    
    extract.write(str(entries) + ' Lines')
    print("End of Reading: read " + str(counter) + " lines. " + str(entries) + " entries with empty values found.")
    
    history = open('imported.imp','a')
    history.write(filename + '\n')
    history.close()
    file.close()
    extract.close()


# EOF
