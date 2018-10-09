# script to define all necessary macros for an OPI screen, giving them
# the values that it finds in other OPIs

import re
import sys
import fileinput
import subprocess

epics_macros = []
ad_macros = []
try:
    print("dir 1: " + sys.argv[1])
    print("dir 2: " + sys.argv[2])
    print("target OPI: " + sys.argv[3])
except IndexError:
    print("Arguments required: ")
    print("\t 1) A directory containing OPI files with macros")
    print("\t 2) Another directory containing OPI files with macros")
    print("\t 3) The target OPI file to put macros in")
    print("python3 addMacros.py OPIs/epics OPIs/ADet/master OPIs/main.opi")
    exit()
dir = sys.argv[1]
arg = "epics/"
list = epics_macros
for i in range(0,4):
    if (i > 1):
        dir = sys.argv[2]
    if (i > 2):
        arg = "epics/"
        list = epics_macros
    print(str(i) + " grep -r " + arg + " " + dir)
    cmd = ["grep", "-r", arg, dir]
    output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0].decode('utf-8')
    macroSearch = re.findall("(<path[a-zA-Z]*>.*</path[a-zA-Z]*>)", output)
    if macroSearch is not None:
        for macro in macroSearch:
            #print(macro)
            if macro not in list:
                list.append(macro)
    arg = "ADet/"
    list = ad_macros

print("EPICS macros:")
for macro in epics_macros:
    print(macro)

print("AD macros:")
for macro in ad_macros:
    print(macro)
    
done = False
print("Adding macros for " + sys.argv[3] + "...")
for lineNum, line in enumerate(fileinput.input(sys.argv[3], inplace=True)):
    if "<macros>" in line and not done:
        macro_str = ""
        for macro in epics_macros:
            macro_str += "\t" + macro + "\n"
        for macro in ad_macros:
            macro_str += "\t" + macro + "\n"
        sys.stderr.write("Added macros: " + macro_str)
        line = line + macro_str
        done = True
    print(line, end="")

