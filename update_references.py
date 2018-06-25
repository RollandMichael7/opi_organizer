# Given a directory of OPI files created by convert_and_organize.py, update the OPI's references to other OPIs so that
# they do not break in the new directory structure; uses macros so that the version of a referenced plugin can be
# chosen at runtime.
# author: Michael Rolland
# version: 2018-06-22


import os
import re
import fileinput
import sys
import subprocess
from urllib.error import URLError
from urllib.request import urlopen

# list of filenames that can not be identified as part of a plugin or ADCore
unidentifiedFiles_dict = {
    # filename : path/to/file
}

# given an OPI file directory created by convert_and_organize.py, update its cross-references.
def cross_reference(opi_dir):
    for root, folders, files in os.walk(opi_dir):
        for file in files:
            if file.endswith(".opi"):
                macro_dict = {}
                plugin = ""
                ver = ""
                folders = os.path.join(root, file)
                folders = folders.split(os.sep)
                tag = str(folders[len(folders)-3])
                print("Updating cross references for " + file + "...")
                sys.stderr.write("Editing " + file + ".\n")
                for lineNum, line in enumerate(fileinput.input(os.path.join(root, file), inplace=True)):
                    # search for <opi_file> tag in the OPI
                    if "<opi_file>" in line:
                        path = re.search("<opi_file>(.*)</opi_file>", line)
                        if path is not None:
                            before = ""
                            after = ""
                            path = path.group(1)
                            if "$" in path:
                               continue
                            sys.stderr.write("line " + str(lineNum + 1) + ": " + line)
                            search = re.search("(.*)<opi_file>", line)
                            if search is not None:
                                before = search.group(1)
                            search = re.search("</opi_file>(.*)", line)
                            if search is not None:
                                after = search.group(1)
                            done = False
                            for top, dirs, filenames in os.walk(opi_dir):
                                if done:
                                    break
                                for filename in filenames:
                                    if filename == path:
                                        folders = os.path.join(top, filename)
                                        folders = folders.split(os.sep)
                                        plugin = str(folders[len(folders) - 3])
                                        ver = str(folders[len(folders) - 2])
                                        done = True
                                        break
                            if plugin != tag:
                                line = before + "<opi_file>" + "$(path" + plugin + ")" + os.sep + \
                                       path + "</opi_file>" + after + "\n"
                                if ("path" + plugin) not in macro_dict.keys():
                                    macro_dict["path" + plugin] = ver
                                sys.stderr.write("converted to: " + line)
                            else:
                                sys.stderr.write("Reference to same plugin left unchanged\n\n")
                    print(line, end="")
                print("References updated.")
                if len(macro_dict.keys()) > 0:
                    add_macros(os.path.join(root,file), macro_dict)


# Called by cross_reference to add the macros into the OPI so that they can be easily seen and used
def add_macros(filePath, macros):
    done = False
    print("Adding macros for " + os.path.basename(filePath) + "...")
    for lineNum, line in enumerate(fileinput.input(filePath, inplace=True)):
        if "<macros>" in line and not done:
            macro_str = ""
            for macro in macros.keys():
                macro_str += "\t<" + macro + ">"
                macro_str += ".." + os.sep + ".." + os.sep + macro +  macros[macro]
                macro_str += "</" + macro + ">" + "\n"
            line = line + macro_str
            done = True
        print(line, end="")


########################### MAIN ###########################
response = ""
config_path = ""
foundOPI_AD = False
foundOPI_EPICS = False

ad_opi_directory = ""
epics_opi_directory = ""

while response != 'y' and response != 'n':
    response = input("Use config file? (y/n) ").lower()
if response == 'y':
    while not os.path.isfile(config_path):
        config_path = input("Enter path to config file: ")
    for line in open(config_path):
        if foundOPI_AD and foundOPI_EPICS:
            break
        if "#" in line:
            continue
        search = re.search("AD_OPI_DIRECTORY : (.*)", line)
        if search is not None and not foundOPI_AD:
            ad_opi_directory = search.group(1)
            if os.path.isdir(ad_opi_directory):
                print("AreaDetector OPI directory: " + ad_opi_directory)
                foundOPI_AD = True
            else:
                print("AreaDetector OPI directory is invalid: " + ad_opi_directory)
                ad_opi_directory = ""
            continue
        search = re.search("EPICS_OPI_DIRECTORY : (.*)", line)
        if search is not None and not foundOPI_EPICS:
            epics_opi_directory = search.group(1)
            if os.path.isdir(epics_opi_directory):
                print("EPICS OPI directory: " + epics_opi_directory)
                foundOPI_EPICS = True
            else:
                print("EPICS OPI directory is invalid: " + epics_opi_directory)
                epics_opi_directory = ""
            continue

# get directory paths
if not foundOPI_AD:
    ad_opi_directory = ""
    while not os.path.isdir(ad_opi_directory):
        ad_opi_directory = input("Enter path to target AreaDetector OPI directory: ")

if not foundOPI_EPICS:
    epics_opi_directory = ""
    while not os.path.isdir(epics_opi_directory):
        epics_opi_directory = input("Enter path to target EPICS modules OPI directory: ")

cross_reference(ad_opi_directory)
cross_reference(epics_opi_directory)
print("Operation complete.")

# print the path to any unidentified files that were found (and thus left untouched)
if len(unidentifiedFiles_dict) != 0:
    print("Unidentified files:")
    for file in unidentifiedFiles_dict.keys():
        print("\t" + file + " (" + unidentifiedFiles_dict[file] + ")")

quit()
