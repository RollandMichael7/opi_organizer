# Given a directory of OPI files created by convert_and_organize.py, update the OPI's references to other OPIs so that
# they do not break in the new directory structure; uses macros so that the version of a referenced plugin can be
# chosen at runtime.
# author: Michael Rolland
# version: 2018-07-03

import glob
import os
import re
import fileinput
import sys
import subprocess
import argparse
from urllib.error import URLError
from urllib.request import urlopen

# list of filenames that can not be identified as part of a plugin or ADCore
unidentifiedFiles_dict = {
    # filename : path/to/file
}

epics_dir = ""
ad_dir = ""

ref2path = {
    # something.opi : [/path/to/something.opi, epics_opi_dir or ad_opi_dir]
}

# given an OPI file directory created by convert_and_organize.py, update its cross-references.
def cross_reference(opi_dir):
    for root, folders, files in os.walk(opi_dir):
        for file in files:
            if file.endswith(".opi"):
                macro_dict = {
                    # plugin name : [plugin version, (areaDetector OR epics-modules), isADet, isLinkToEpics]
                    # isADet: True iff the plugin being updated is part of an AreaDetector plugin
                    # isLinkToEpics: True iff the plugin being updated is part of an AreaDetector plugin
                    #                AND the OPI being linked to is part of an EPICS module
                }
                folders = os.path.join(root, file)
                folders = folders.split(os.sep)
                tag = str(folders[len(folders)-3])
                print("Updating cross references for " + file + "...")
                sys.stderr.write("Editing " + file + ".\n")
                for lineNum, line in enumerate(fileinput.input(os.path.join(root, file), inplace=True)):
                    # search for <opi_file> tag in the OPI
                    if "<opi_file>" in line or "<path>" in line:
                        plugin = ""
                        ver = ""
                        pluginType = ""
                        foundIn = ""
                        if "<opi_file>" in line:
                            pathTag = "opi_file"
                        else:
                            pathTag = "path"
                        path = re.search(pathTag + ">(.*)</" + pathTag + ">", line)
                        if path is not None:
                            before = ""
                            after = ""
                            path = path.group(1)
                            if "$" in path:
                                print(line, end="")
                                continue
                            sys.stderr.write("line " + str(lineNum + 1) + ": " + line)
                            search = re.search("(.*)<" + pathTag + ">", line)
                            if search is not None:
                                before = search.group(1)
                            search = re.search("</" + pathTag + ">(.*)", line)
                            if search is not None:
                                after = search.group(1)
                            if path in ref2path.keys():
                                folders = ref2path[path][0]
                                folders = folders.split(os.sep)
                                pluginType = str(folders[len(folders) - 4])
                                plugin = str(folders[len(folders) - 3])
                                ver = str(folders[len(folders) - 2])
                                foundIn = ref2path[path][1]
<<<<<<< HEAD
                                # if opi_dir == epics_dir and foundIn == ad_dir:
                                #    pluginType = str(folders[len(folders) - 5]) + os.sep + str(folders[len(folders) - 4])
=======
                                if foundIn == ad_dir:
                                    pluginType = str(folders[len(folders) - 5]) + os.sep + str(folders[len(folders) - 4])
>>>>>>> master
                            else:
                                done = False
                                if path.startswith("AD") or path.startswith("ND"):
                                    first = ad_dir
                                    second = epics_dir
                                else:
                                    first = epics_dir
                                    second = ad_dir
                                lookIn = first
                                while not done:
                                    for top, dirs, filenames in os.walk(lookIn):
                                        if done:
                                            break
                                        for filename in filenames:
                                            if filename == path:
                                                folders = os.path.join(top, filename)
                                                ref2path[path] = [folders, lookIn]
                                                folders = folders.split(os.sep)
                                                pluginType = str(folders[len(folders) - 4])
                                                # sys.stderr.write("type: " + pluginType + "\n")
                                                plugin = str(folders[len(folders) - 3])
                                                ver = str(folders[len(folders) - 2])
                                                done = True
                                                foundIn = lookIn
<<<<<<< HEAD
                                                # if opi_dir == epics_dir and foundIn == ad_dir:
                                                #    pluginType = str(folders[len(folders) - 5]) + os.sep + str(folders[len(folders) - 4])
=======
                                                if foundIn == ad_dir:
                                                    pluginType = str(folders[len(folders) - 5]) + os.sep + str(folders[len(folders) - 4])
>>>>>>> master
                                                break
                                    if lookIn == second and not done or (lookIn == first and first == second and not not done):
                                        break
                                    if done:
                                        break
                                    lookIn = second
                                if not done:
                                    sys.stderr.write("Could not identify reference. Left unchanged\n")
                            if plugin != "":
                                if plugin != tag and plugin != "" and tag != "":
                                    line = before + "<" + pathTag + ">"+ ".." + os.sep + ".." + os.sep + ".." + os.sep
                                    if opi_dir == ad_dir:
                                        line = line + ".." + os.sep
                                    line = line + "$(path" + plugin[:1].upper() + plugin[1:] + ")" + os.sep + path + "</" + pathTag + ">" + after + "\n"
                                    if plugin not in macro_dict.keys():
                                        # if opi_dir == ad_dir:
                                        #     isADet = True
                                        # else:
                                        #     isADet = False
                                        # if isADet and foundIn == epics_dir:
                                        #     isLinkToEpics = True
                                        # else:
                                        #     isLinkToEpics = False
                                        macro_dict[plugin] = [ver, pluginType]
                                    sys.stderr.write("converted to: " + line)
                                else:
                                    sys.stderr.write("Reference to same plugin left unchanged\n")
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
                # isADet = macros[macro][2]
                # isLinkToEpics = macros[macro][3]
                macro_str += "\t<" + "path" + macro[:1].upper() + macro[1:] + ">"
                # if isADet and isLinkToEpics:
                #     macro_str += ".." + os.sep
<<<<<<< HEAD
                macro_str += ".." + os.sep + ".." + os.sep + ".." + os.sep + macros[macro][1] + os.sep\
                             + macro + os.sep + macros[macro][0]
=======
                #macro_str += ".." + os.sep + ".." + os.sep + ".." + os.sep + macros[macro][1] + os.sep\
                #             + macro + os.sep + macros[macro][0]
                macro_str += macros[macro][1] + os.sep + macro + os.sep + macros[macro][0]
>>>>>>> master
                macro_str += "</" + "path" +  macro[:1].capitalize() + macro[1:] + ">" + "\n"
            sys.stderr.write("Added macros: " + macro_str)
            line = line + macro_str
            done = True
        print(line, end="")


########################### MAIN ###########################
response = ""
config_path = ""
foundOPI_AD = False
foundOPI_EPICS = False
forced = False

parser = argparse.ArgumentParser(description="Update references between OPI files")
parser.add_argument('-f', dest='config_path', help="Bypass confirmation prompts. Requires a path to a config file")
parser.add_argument('config', nargs='?', default="", help="Path to a config file.")
parsed_args = parser.parse_args()

if parsed_args.config_path is not None:
    config_path = parsed_args.config_path
    if not os.path.isfile(config_path):
        print("Invalid path: " + config_path)
        exit()
    forced = True
elif parsed_args.config != "":
    config_path = parsed_args.config
    if not os.path.isfile(config_path):
        print("Invalid path: " + config_path)
        config_path = ""

if config_path == "":
    while response != 'y' and response != 'n':
        response = input("Use config file? (y/n) ").lower()
    if response == 'y':
        while not os.path.isfile(config_path):
            config_path = input("Enter path to config file: ")
if config_path != "":
    for line in open(config_path):
        if foundOPI_AD and foundOPI_EPICS:
            break
        if "#" in line:
            continue
        search = re.search("AD_OPI_DIRECTORY : (.*)", line)
        if search is not None and not foundOPI_AD:
            ad_dir = search.group(1)
            if os.path.isdir(ad_dir):
                print("AreaDetector OPI directory: " + ad_dir)
                foundOPI_AD = True
            else:
                print("AreaDetector OPI directory is invalid: " + ad_dir)
                ad_dir = ""
            continue
        search = re.search("EPICS_OPI_DIRECTORY : (.*)", line)
        if search is not None and not foundOPI_EPICS:
            epics_dir = search.group(1)
            if os.path.isdir(epics_dir):
                print("EPICS OPI directory: " + epics_dir)
                foundOPI_EPICS = True
            else:
                print("EPICS OPI directory is invalid: " + epics_dir)
                epics_dir = ""
            continue

# get directory paths
if not foundOPI_AD and not forced:
    ad_dir = ""
    while not os.path.isdir(ad_dir):
        ad_dir = input("Enter path to target AreaDetector OPI directory: ")

if not foundOPI_EPICS and not forced:
    epics_dir = ""
    while not os.path.isdir(epics_dir):
        epics_dir = input("Enter path to target EPICS modules OPI directory: ")

if not os.path.isdir(ad_dir):
    print("Invalid directory: " + ad_dir)
    exit()
if not os.path.isdir(epics_dir):
    print("Invalid directory: " + epics_dir)
    exit()

cross_reference(ad_dir)
cross_reference(epics_dir)
print("Operation complete.")

# print the path to any unidentified files that were found (and thus left untouched)
if len(unidentifiedFiles_dict) != 0:
    print("Unidentified files:")
    for file in unidentifiedFiles_dict.keys():
        print("\t" + file + " (" + unidentifiedFiles_dict[file] + ")")

quit()
