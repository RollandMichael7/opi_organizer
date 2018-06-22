import os
import re
import fileinput
import sys
from urllib.error import URLError
from urllib.request import urlopen
from shutil import copyfile

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

# path to Control Systems Studio executable, used for converting adl files to opi files
css_path = ""


# Convert MEDM adl files to BOY opi files using CS Studio, and store those files in the new directory
def convert_adls(ad_dir, opi_dir):
    # arguments used in executing CS Studio
    css_dict = {
        # /path/to/adl/file : [plugin name, plugin version]
    }
    file2plug =  {
        # converted opi filename : [plugin name, plugin version, plugin key]
    }
    for root, dirs, files in os.walk(ad_dir):
        for file in files:
            if file.endswith(".adl"):
                print(file)
                plugin = ""
                ver = ""
                tag = ""
                # identify which plugin the adl belongs to
                if "ADCore" in os.path.join(root, file):
                    plugin = "ADCore"
                    ver = ADCore_ver
                    tag = None
                else:
                    for p in plugin_dict.keys():
                        if plugin_dict[p][0] in os.path.join(root, file):
                            if plugin_dict[p][0] == "ADAndor" and "Andor3" in os.path.join(root, file):
                                continue
                            plugin = plugin_dict[p][0]
                            ver = plugin_dict[p][1]
                            tag = p
                            break
                # if it was identified, check if its already been converted previously
                # (to avoid executing CS Studio too much)
                if plugin != "" and ver != "":
                    newPath = opi_dir + os.sep + plugin + os.sep + ver
                    opi = file[:-4] + ".opi"
                    # if <filename>.opi already exists in the OPI folder, it has been converted and moved
                    # already (adl files are not removed after being converted)
                    if os.path.isfile(newPath + os.sep + opi):
                        print("File has already been converted.")
                        continue
                    # if <filename>.opi already exists in the adl folder, it has been converted but
                    # not moved, so it is deleted and converted/moved again for simplicity
                    if os.path.isfile(os.path.join(root,file)[:-4] + ".opi"):
                        os.remove(os.path.join(root,file)[:-4] + ".opi")
                    css_dict[os.path.join(root, file)] = [plugin, ver]
                    if plugin != "ADCore":
                        file2plug[file[:-4] + ".opi"] = [plugin, ver, tag]
                        # print("key: " + file[:-4] + ".opi")
    if len(css_dict) > 3:
        try:
            print("Executing CS Studio...")
            args = css_path + " -nosplash -application org.csstudio.opibuilder.adl2boy.application"
            for arg in css_dict.keys():
                args = args + " " + arg
            # run(list(css_dict.keys()))
            os.system(args)
        except OSError:
            print("Could not run CS Studio. It may not have the adl2boy feature.")
            return
        for file in list(css_dict.keys())[3:]:
            if css_dict[file] == "":
                continue
            # print(file)
            opi = file[:-4] + ".opi"
            # print(opi)
            newPath = opi_dir + os.sep + css_dict[file][0] + os.sep + css_dict[file][1]
            if not os.path.exists(newPath):
                os.makedirs(newPath)
            newPath = newPath + os.sep + os.path.basename(opi)
            # print("move: " + opi + " -> " + newPath)
            os.rename(opi, newPath)
            # print("opi: " + opi)


# given a directory of Area Detector files, construct a hierarchical directory that
# groups OPIs into their respective plugins and versions
def organize(ad_dir, opi_dir):
    ver = ""
    dirName = ""
    for root, dirs, files in os.walk(ad_dir):
        for file in files:
            if os.path.isfile(os.path.join(root, file)) and file.endswith('.opi'):
                old = False
                if opi_dir in os.path.join(root, file):
                    old = True
                # check if the opi file matches one of the
                # plugins being searched for
                isPlugin = False
                if "ADCore" in os.path.join(root, file):
                    dirName = "ADCore"
                    ver = ADCore_ver
                    print("Found ADCore file: " + file + " (" + os.path.join(root, file) + ")")
                else:
                    for plugin in plugin_dict.keys():
                        if plugin in os.path.join(root, file):
                            if plugin == "ADAndor" and "ADAndor3" in os.path.join(root,file):
                                continue
                            isPlugin = True
                            # print("Found plugin file: " + file)
                            dirName = plugin_dict.get(plugin)[0]
                            ver = plugin_dict.get(plugin)[1]
                            print("Found " + dirName + " file: " + file + " (" + os.path.join(root, file) + ")")
                            break
                if isPlugin is False and dirName != "ADCore":
                    unidentifiedFiles_dict[file] = os.path.join(root, file)
                    continue
                # construct new location of organized file
                newPath = opi_directory + os.sep + dirName + os.sep + ver
                oldPath = os.path.join(root, file)
                # print("current path: " + oldPath)
                if not os.path.exists(newPath):  # create new folder if it doesn't exist
                    # print("making new folder...")
                    os.makedirs(newPath)
                newPath = newPath + os.sep + file
                if oldPath != newPath and not os.path.isfile(newPath):  # if the file isn't already in its folder, move it
                    # print("new path: " + newPath)
                    # print("old path: " + oldPath)
                    if not old:
                        print("File copied")
                        copyfile(oldPath, newPath)
                    else:
                        print("File moved")
                        os.rename(oldPath, newPath)
                else:
                    print("File is already organized.")
    # do same thing for opi directory
    directory = opi_dir
    for file in os.listdir(opi_dir):
        if os.path.isfile(os.path.join(opi_dir, file)) and file.endswith(".opi"):
            isPlugin = False
            for plugin in plugin_dict.keys():
                if plugin.casefold() in file.casefold():
                    if plugin == "Andor" and "Andor3" in file:
                        continue
                    isPlugin = True
                    # print("Found plugin file: " + file)
                    dirName = plugin_dict.get(plugin)[0]
                    ver = plugin_dict.get(plugin)[1]
                    print("Found " + dirName + " file: " + file + " (" + os.path.join(opi_dir, file) + ")")
                    break
            if isPlugin is False:
                if "AD" in file or "ND" in file or "commonPlugins" in file:
                    dirName = "ADCore"
                    ver = ADCore_ver
                    print("Found ADCore file: " + file + " (" + os.path.join(opi_dir, file) + ")")
                else:
                    unidentifiedFiles_dict[file] = os.path.join(opi_dir, file)
                    continue
            newPath = directory + os.sep + dirName + os.sep + ver
            oldPath = os.path.join(directory, file)
            # print("current path: " + oldPath)
            if not os.path.exists(newPath):
                print("making new folder...")
                os.makedirs(newPath)
            newPath = newPath + os.sep + file
            if oldPath != newPath:
                # print("new path: " + newPath)
                try:
                    os.rename(oldPath, newPath)
                except FileExistsError:
                    # if file exists in both new and old directory, remove old one
                    os.remove(oldPath)
                    print("File already exists.")
                    continue
                print("File moved.")
            else:
                print("File is already organized.")


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
        if foundOPI and foundAD and foundCSS:
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
        search = re.search("CSS_PATH : (.*)", line)
        if search is not None and not foundCSS:
            css_path = search.group(1)
            if os.path.isfile(css_path):
                print("CSS path: " + css_path)
                foundCSS = True
            else:
                print("CSS path is invalid: " + css_path)
                css_path = ""
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

if not foundCSS:
    # ask user if they want to use the CS Studio adl2boy feature, get path to executable if so
    print("If installed, CS Studio can be used to convert MEDM adl files into BOY opi files.")
    response = ""
    while response != 'y' and response != 'n':
        response = input("Use this feature? (y/n) ").lower()
    if response == 'y':
        while not os.path.isfile(css_path):
            css_path = input("Enter path to CSS executable: ")

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
if css_path != "":
    print("Converting adl files...")
    convert_adls(ad_directory, opi_directory)
print("\nAll ADL files converted.\n")

organize(ad_directory, opi_directory)
print("\nDirectory successfully updated.\n")

# print the path to any unidentified files that were found (and thus left untouched)
if len(unidentifiedFiles_dict) != 0:
    print("Unidentified files:")
    for file in unidentifiedFiles_dict.keys():
        print("\t" + file + " (" + unidentifiedFiles_dict[file] + ")")
quit()

