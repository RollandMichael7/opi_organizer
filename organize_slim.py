# Given a "flat" directory of Area Detector OPI files, convert it to a hierarchical directory that groups OPIs
# into plugins and versions. Simultaneously, update any cross-references in the OPI files to be consistent with the
# new directory structure so that they don't break. Also may use CS Studio to convert MEDM adl files into OPIs.
# author: Michael Rolland
# version: 2018-06-22

import os
import re
import fileinput
import sys
from urllib.error import URLError
from urllib.request import urlopen

# example dict of some Area Detector plugins
# dict matches filename substring with plugin name and version
plugin_dict = {
    # "andor"      : ["ADAndor3", "R2-2"],
    # "dexela"     : ["ADDexela", "R2-1"],
    # "eiger"      : ["ADEiger", "R2-5"],
    # "pilatus"    : ["ADPilatus", "R2-5"],
    # "prosilica"  : ["ADProsilica", "R2-4"],
    # "simdetector": ["ADSimDetector", "R2-7"],
}

# list of Area Detector plugins, populated by searching the github repository
plugin_list = []

# list of filenames that can not be identified as part of a plugin or ADCore, populated by organize()
unidentifiedFiles_dict = {
    # filename : path/to/file
}

# version of ADCore used
ADCore_ver = ""

# Default constants to circumvent asking for user input. Set to None to ask for input
DEFAULT_OPI_DIRECTORY = None

DEFAULT_AD_DIRECTORY = None

# given a flat directory of Area Detector OPIs, convert it to a hierarchical directory that
# groups OPIs into their respective plugins and versions
def organize(directory):
    ver = ""
    tag = ""
    dirName = ""
    for file in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file)) and file.endswith('.opi'):
            # check if the opi file matches one of the
            # plugins being searched for
            isPlugin = False
            for plugin in plugin_dict.keys():
                if plugin.casefold() in file.casefold():
                    isPlugin = True
                    print("Found plugin file: " + file)
                    dirName = plugin_dict.get(plugin)[0]
                    tag = plugin
                    ver = plugin_dict.get(plugin)[1]
                    print("plugin name: " + dirName)
                    break
            # else, it is either a part of ADCore or unidentifiable
            if isPlugin is False:
                if "AD" in file or "ND" in file or "commonPlugins" in file:
                    dirName = "ADCore"
                    ver = ADCore_ver
                    print("Found ADCore file: " + file)
                else:
                    unidentifiedFiles_dict[file] = os.path.join(directory, file)
                    continue
            # construct new location of organized file
            newPath = directory + os.sep + dirName + os.sep + ver
            oldPath = os.path.join(directory, file)
            print("current path: " + oldPath)
            if not os.path.exists(newPath):  # create new folder if it doesn't exist
                print("making new folder...")
                os.makedirs(newPath)
            newPath = newPath + os.sep + file
            if oldPath != newPath:  # if the file isn't already in its folder, move it
                print("new path: " + newPath)
                if isPlugin is True:
                    cross_reference(directory, file, tag)
                    print("References updated.")
                os.rename(oldPath, newPath)
                print("File moved.")
            else:
                print("file is already organized.")
            # print("\n")


# given an OPI file moved by organize(), update its cross-references. The "tag" argument is the identifying
# substring for the plugin "file" belongs to
def cross_reference(root, file, tag):
    print("Updating cross references for " + file + "...")
    sys.stderr.write("Editing " + file + ". If the program exits before completion a .bak "
                                         "backup of the original is created.\n")
    for lineNum, line in enumerate(fileinput.input(os.path.join(root, file), inplace=True)):
        # search for <opi_file> tag in the OPI
        if "<opi_file>" in line:
            path = re.search("<opi_file>(.*)</opi_file>", line)
            if path is not None:
                newPath = ""
                before = ""
                after = ""
                path = path.group(1)
                sys.stderr.write("line " + str(lineNum + 1) + ": " + line)
                # ignore reference to OPI of the same plugin
                # (does not need to be changed)
                if tag.casefold() in path.casefold():
                    sys.stderr.write("Reference to same plugin left unchanged\n\n")
                    print(line, end="")
                    continue
                search = re.search("(.*)<opi_file>", line)
                if search is not None:
                    before = search.group(1)
                search = re.search("</opi_file>(.*)", line)
                if search is not None:
                    after = search.group(1)
                if "AD" in path or "ND" in path:
                    newPath = "ADCore" + os.sep + ADCore_ver
                else:
                    for plugin in plugin_dict.keys():
                        if plugin.casefold() in path.casefold():
                            newPath = plugin_dict.get(plugin)[0] + os.sep + plugin_dict.get(plugin)[1]
                            break
                if newPath != "":
                    line = before + "<opi_file>" + ".." + os.sep + ".." + os.sep + newPath \
                           + os.sep + path + "</opi_file>" + after + "\n"
                else:
                    sys.stderr.write("Tag can not be identified; routed to original directory\n\n")
                    line = before + "<opi_file>" + ".." + os.sep + ".." + os.sep + path + "</opi_file>" + after + "\n"
                sys.stderr.write("converted to: " + line)
        print(line, end="")
    print("Updated.")


# prompt the user to register a plugin into the search dictionary, using "suggestion" (if not None)
#  as a suggested search term
def register_plugin(plugin, suggestion):
    ver = input("Enter version for " + plugin + ": ")
    key = ""
    if suggestion is None:
        key = input("Enter filename substring to identify OPIs with: ")
    else:
        while key != 'y' and key != 'n':
            key = input('Use "' + suggestion + '" as filename substring for identifying OPIs? (y/n) ').lower()
        if key == 'y':
            key = suggestion
        else:
            key = input("Enter filename substring to identify OPIs with: ")
    plugin_dict[key] = [plugin, ver]
    print(plugin + " " + ver + " registered in search.")


# do a case-insensitive search in "directory" for OPI files with the substring "query" in the name
def search_directory(directory, query):
    for file in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file)) and file.endswith('.opi'):
            if query.casefold() in file.casefold():
                return True
    return False


########################### MAIN ###########################
response = ""
config_path = ""
foundOPI = False
foundAD = False
foundCSS = False

opi_directory = ""
ad_directory = ""

while response != 'y' and response != 'n':
    response = input("Use config file? (y/n) ").lower()
if response == 'y':
    while not os.path.isfile(config_path):
        config_path = input("Enter path to config file: ")
    for line in open(config_path):
        if foundOPI and foundAD:
            break
        if "#" in line:
            continue
        search = re.search("OPI_DIRECTORY : (.*)", line)
        if search is not None and not foundOPI:
            opi_directory = search.group(1)
            if os.path.isdir(opi_directory):
                print("OPI directory: " + opi_directory)
                foundOPI = True
            else:
                print("OPI directory is invalid: " + opi_directory)
                opi_directory = ""
            continue
        search = re.search("AD_DIRECTORY : (.*)", line)
        if search is not None and not foundAD:
            ad_directory = search.group(1)
            if os.path.isdir(ad_directory):
                print("AD directory: " + ad_directory)
                foundAD = True
            else:
                print("AD directory is invalid: " + ad_directory)
                ad_directory = ""
            continue

# get directory paths
if not foundOPI:
    opi_directory = ""
    while not os.path.isdir(opi_directory):
        opi_directory = input("Enter path to target OPI directory: ")

if not foundAD:
    ad_directory = ""
    while not os.path.isdir(ad_directory):
        ad_directory = input("Enter path to AreaDetector directory containing plugins: ")

core_path = ad_directory + os.sep + "ADCore" + os.sep + "RELEASE.md"
try:
    search = False
    core = open(core_path)
    for line in core:
        if "Release Notes" in line:
            search = True
            continue
        if search is True:
            core_ver = re.search("(R\d+-\d+(?:-\d+)*)", line)
            if core_ver is not None:
                ADCore_ver = core_ver.group(1)
                print("Detected ADCore " + ADCore_ver)
                break
except IOError:
    print("Could not detect ADCore version.")
    ADCore_ver = input("Enter ADCore version: ")

# search the github repository for AreaDetector plugins; compare against the user's AreaDetector directory
# and prompt the user to confirm the existence of any matches found (as well as the version if it can not be found)
matches = []
currPage = 0
error = False
start = True
print("Detecting plugins...")
while len(matches) != 0 or start is True:
    start = False
    currPage += 1
    repo_string = 'https://github.com/areaDetector?page=' + str(currPage)
    try:
        repo = urlopen(repo_string).read().decode('utf-8')
    except URLError:
        print("ERROR: Can not access github.")
        error = True
        break
    matches = re.findall("a href=\"/areaDetector/(.*)\" itemprop", repo)
    for match in matches:
        skip = False
        ver = ""
        if match != "ADCore" and match != "areaDetector":
            if config_path != "":
                for line in open(config_path):
                    if "#" in line:
                        continue
                    if match.casefold() in line.casefold():
                        skip = True
                        verSearch = re.search(match + " : " + "(.*)", line)
                        if verSearch is not None:
                            ver = verSearch.group(1)
                        break
            response = ""
            plugin_list.append(match)
            release_path = ad_directory + os.sep + match + os.sep + "RELEASE.md"
            try:
                search = False
                release = open(release_path)
                found = False
                for line in release:
                    if ver != "":
                        found = True
                        if match.startswith("AD"):
                            plugin_dict[match[2:]] = [match, ver]
                        else:
                            plugin_dict[match] = [match, ver]
                        print("Registered " + match + " " + ver)
                        break
                    if "Release Notes" in line:
                        search = True
                        continue
                    if search is True:
                        version = re.search("(R\d+-\d+(?:-\d+)*)", line)
                        if version is not None:
                            found = True
                            response = ""
                            plugin_ver = version.group(1)
                            if skip is False:
                                while response != 'y' and response != 'n':
                                    response = input("Register " + match + " version " + plugin_ver + "? (y/n) ").lower()
                            if response == 'y' or skip is True:
                                if match.startswith("AD"):
                                    plugin_dict[match[2:]] = [match, plugin_ver]
                                else:
                                    plugin_dict[match] = [match, plugin_ver]
                                if skip is True:
                                    print("Registered " + match + " " + plugin_ver)
                            break
                if found is False:
                    ver = ""
                    if config_path != "":
                        for line in open(config_path):
                            if "#" in line:
                                continue
                            if match in line:
                                verSearch = re.search(match + " : " + "(.*)", line)
                                if verSearch is not None:
                                    ver = verSearch.group(1)
                                    break
                    if ver == "":
                        while response != 'y' and response != 'n':
                            response = input("Detected " + match + " but could not find version. Register and "
                                       "confirm version? (y/n) ").lower()
                        if response == 'y':
                            ver = input("Enter version: ")
                        else:
                            continue
                    if match.startswith("AD"):
                        plugin_dict[match[2:]] = [match, ver]
                    else:
                        plugin_dict[match] = [match, ver]
                    if skip is True:
                        print("Registered " + match + " " + ver)
            except IOError:
                release_path = ad_directory + os.sep + match
                if os.path.isdir(release_path):
                    if config_path != "":
                        for line in open(config_path):
                            if match in line:
                                verSearch = re.search(match + " : " + "(.*)", line)
                                if verSearch is not None:
                                    ver = verSearch.group(1)
                                    break
                    if ver == "":
                        while response != 'y' and response != 'n':
                            response = input("Detected " + match + " but could not find version. Register and "
                                       "confirm version? (y/n) ").lower()
                        if response == 'y':
                            ver = input("Enter version: ")
                        else:
                            continue
                    if match.startswith("AD"):
                        plugin_dict[match[2:]] = [match, ver]
                    else:
                        plugin_dict[match] = [match, ver]
                    if skip is True:
                        print("Registered " + match + " " + ver)

# after comparing user's local directory against the github repo, ask the user if they want to manually register any
# more plugins into the search
if error is False:
    print("Done detecting plugins.")
    choice = ""
    substr = ""
    query = ""
    while query != "done":
        response = ""
        choice = ""
        found = False
        query = input("Search for a plugin (or enter \"done\" to stop registering plugins): ")
        if query.lower() == "done":
            break
        match_list = []
        for plugin in plugin_list:
            if query.casefold() in plugin.casefold():
                found = True
                match_list.append(plugin)
                if query.casefold() == plugin.casefold():
                    print(plugin + " found.")
                    choice = plugin
                    break
                print(plugin)
        if found is True:
            while choice not in match_list and choice.lower() != "back" and choice.lower() != "reg":
                choice = input('Enter plugin to register (or "back" to search again or "reg"'
                               ' to register search term): ')
            if choice.lower() == "back":
                continue
            if choice.lower() == "reg":
                choice = query
            register_plugin(choice, None)
        else:
            while response != 'y' and response != 'n':
                response = input("Plugin " + query + " not found. Register it anyway? (y/n) ").lower()
            if response == 'y':
                register_plugin(query, None)

# if the github site could not be connected to for some reason, the user must input all their plugins manually
else:
    print("Plugins must be entered manually.")
    plugin = input("Enter a plugin to register (or \"done\" to stop adding plugins): ")
    while plugin != "done":
        version = input("Enter version: ")
        substr = input("Enter filename substring to search for: ")
        plugin_dict[substr] = [plugin, version]
        print(plugin + " version " + version + " added to search, identifying with \"" + substr + "\".")
        plugin = input("Enter plugin to search for (or \"done\" to stop adding plugins): ")

# do the organizing
organize(opi_directory)

print("\nDirectory successfully updated.\n")

# print the path to any unidentified files that were found (and thus left untouched)
if len(unidentifiedFiles_dict) != 0:
    print("Unidentified files:")
    for file in unidentifiedFiles_dict.keys():
        print("\t" + file + " (" + unidentifiedFiles_dict[file] + ")")
quit()