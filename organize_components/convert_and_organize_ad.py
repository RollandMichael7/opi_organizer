# Given an Area Detector repository, a folder for OPI files, and CS Studio, converts MEDM adl files from the AD repo
# into OPIs and organize them into a hierarchical directory that groups by plugin and version.
# This will break any references from an OPI of one plugin to an OPI of another (such as any reference to ADCore),
# which can be fixed with update_references.py
# author: Michael Rolland
# version: 2018.10.05


import os
import re
import fileinput
import sys
import subprocess
import argparse
from urllib.error import URLError
from urllib.request import urlopen
from shutil import copyfile

# dict matches plugin name with plugin version
plug2ver = {
    # plugin name : plugin version
}

folder2plugin = {
    # folder name : plugin name
}

# list of Area Detector plugins, populated by searching the github repository
plugin_list = []

# list of plugins to ignore
blacklist = []

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
    for folder in folder2plugin.keys():
        for root, dirs, files in os.walk(os.path.join(ad_dir, folder)):
            for file in files:
                if file.endswith(".adl"):
                    print(file)
                    # identify which plugin the adl belongs to
                    plugin = folder2plugin[folder]
                    ver = plug2ver[plugin]
                    # if it was identified, check if its already been converted previously
                    # (to avoid executing CS Studio too much)
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
                    file2plug[file[:-4] + ".opi"] = [plugin, ver]
    if len(css_dict) > 0:
        i = 0
        done = False
        try:
            while not done:
                print("Executing CS Studio...")
                args = css_path + " -nosplash -application org.csstudio.opibuilder.adl2boy.application"
                adl = list(css_dict.keys())
                while i < len(adl):
                    if len(args + adl[i]) > 8100:
                        break
                    args = args + " " + adl[i]
                    i += 1
                if i == len(adl):
                    done = True
                os.system(args)
        except OSError:
            print("Could not run CS Studio. It may not have the adl2boy feature.")
            return
        for file in list(css_dict.keys()):
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
    if not os.path.isdir(ad_dir):
        print("Invalid directory: " + ad_dir)
        return
    if not os.path.isdir(opi_dir):
        print("Invalid directory: " + opi_dir)
        return
    for folder in folder2plugin.keys():
        for root, dirs, files in os.walk(os.path.join(ad_dir, folder)):
            for file in files:
                if os.path.isfile(os.path.join(root, file)) and file.endswith('.opi'):
                    old = False
                    if opi_dir in os.path.join(root, file):
                        old = True
                    plugin = folder2plugin[folder]
                    ver = plug2ver[plugin]
                    print("Found " + plugin + " file: " + file + " (" + os.path.join(root, file) + ")")
                    # construct new location of organized file
                    newPath = opi_directory + os.sep + plugin + os.sep + ver
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


def skipPlugin(path, plugin):
    if plugin == "ADAndor" and "Andor3" in path:
        return True
    return False


def registerExtraPlugins(config):
    print("looking for extra plugins...")
    start = False
    for line in open(config):
        if "#" in line:
            continue
        if "BEGIN_AD" in line:
            start = True
        if "END_AD" in line:
            return
        if start:
            if "+AD: " in line:
                search = re.search("\+AD: (.*)", line)
                if search is not None:
                    split = search.group(1).split(" ")
                    folder = findFolder(split[0])
                    if folder is None:
                        print("Could not find a folder for " + split[0] + ".")
                        continue
                    if len(split) < 2:
                        ver = "R1-0"
                        print("Could not find version for " + split[0] + ". Defaulting to R1-0")
                    else:
                        ver = split[1]
                    register(split[0], ver, folder)

def blacklistPlugins(config):
    print("blacklisting...")
    start = False
    for line in open(config):
        if "#" in line:
            continue
        if "BEGIN_AD" in line:
            start = True
        if "END_AD" in line:
            return
        if start:
            if line.startswith("-"):
                search = re.search("-([^ ]*)", line)
                if search is not None:
                    plugin = search.group(1).strip()
                    print("Ignoring " + plugin)
                    blacklist.append(plugin)


def register(plugin, ver, folder):
    plug2ver[plugin] = ver
    folder2plugin[folder] = plugin
    print("Registered " + plugin + " " + ver + " in " + folder)


def findFolder(plugin):
    for folder in os.listdir(ad_directory):
        if skipPlugin(folder, plugin):
            continue
        if plugin.casefold() in folder.casefold():
            return folder
    return None


########################### MAIN ###########################
response = ""
config_path = ""
foundOPI = False
foundAD = False
foundCSS = False
forced = False

ad_directory = ""
opi_directory = ""

parser = argparse.ArgumentParser(description="Convert AreaDetector plugin ADL files into OPIs and organize them.")
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
        exit()

if config_path == "":
    while response != 'y' and response != 'n':
        response = input("Use config file? (y/n) ").lower()
    if response == 'y':
        while not os.path.isfile(config_path):
            config_path = input("Enter path to config file: ")

if config_path != "":
    blacklistPlugins(config_path)
    for line in open(config_path):
        if foundOPI and foundAD and foundCSS:
            break
        if "#" in line:
            continue
        search = re.search("AD_OPI_DIRECTORY : (.*)", line)
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
if not foundOPI and not forced:
    opi_directory = ""
    while not os.path.isdir(opi_directory):
        opi_directory = input("Enter path to target OPI directory: ")

if not foundAD and not forced:
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
    if not forced:
        print("Could not detect ADCore version.")
        ADCore_ver = input("Enter ADCore version: ")

if not foundCSS and not forced:
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
startLoop = True
print("Detecting plugins...")
while len(matches) != 0 or startLoop is True:
    startLoop = False
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
        if match in blacklist:
            continue
        whitelisted = False
        ver = ""
        response = ""
        folder = findFolder(match)
        if folder is None:
            continue
        plugin_list.append(match)
        if config_path != "":
            start = False
            for line in open(config_path):
                if "#" in line:
                    continue
                if "BEGIN_AD" in line:
                    start = True
                if "END_AD" in line:
                    break
                if start:
                    if match.casefold() in line.casefold():
                        whitelisted = True
                        verSearch = re.search(match + " : " + "(.*)", line)
                        if verSearch is not None:
                            ver = verSearch.group(1)
                        break
        if ver != "":
            register(match, ver, folder)
            continue
        release_path = ad_directory + os.sep + folder
        dirPath = os.path.abspath(release_path) + os.sep + ".git"
        command = ["git", "--git-dir=" + dirPath, "describe", "--tags"]
        output = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0].decode('utf-8')
        verSearch = re.search("(\d+-\d+(?:-\d+)*)", output)
        if verSearch is not None:
            ver = verSearch.group(1)
            ver = "R" + ver
            response = ""
            while response != 'y' and response != 'n' and not forced:
                response = input("Register " + match + " " + ver + "? (y/n) ")
            if response == 'y' or whitelisted is True:
                register(match, ver, folder)
            continue
        else:
            response = ""
            output = ""
            verSearch = None
            print("Could not get version from git command: git --git-dir=" + dirPath + " describe --tags")
        release_path = ad_directory + os.sep + folder + os.sep + "RELEASE.md"
        try:
            search = False
            found = False
            release = open(release_path)
            for line in release:
                if "Release Notes" in line:
                    search = True
                    continue
                if search is True:
                    version = re.search("(R\d+-\d+(?:-\d+)*)", line)
                    if version is not None:
                        found = True
                        response = ""
                        plugin_ver = version.group(1)
                        if whitelisted is False and not forced:
                            while response != 'y' and response != 'n':
                                response = input("Register " + match + " version " + plugin_ver + "? (y/n) ").lower()
                        if response == 'y' or whitelisted is True:
                            register(match, plugin_ver, folder)
                        break
        except FileNotFoundError:
            print()
        if ver != "":
            continue
        while response != 'y' and response != 'n':
            response = input("Detected " + match + " but could not find version. Register and "
                                                   "confirm version? (y/n) ").lower()
        if response == 'n':
            continue
        ver = input("Enter version: ")
        register(match, ver, folder)

if config_path != "":
    registerExtraPlugins(config_path)

# after comparing user's local directory against the github repo, ask the user if they want to manually register any
# more plugins into the search
if error is False:
    print("Done detecting plugins.")
    choice = ""
    substr = ""
    query = ""
    while query != "done" and not forced:
        folder = ""
        response = ""
        choice = ""
        found = False
        query = input('Search for a plugin (or enter "done" to stop registering plugins): ')
        if query.lower() == "done":
            break
        match_list = []
        for plugin in plugin_list:
            if query.casefold() in plugin.casefold():
                found = True
                match_list.append(plugin)
                if query.casefold() == plugin.casefold():
                    folder = findFolder(plugin)
                    if folder is None:
                        print("No folder found for " + plugin)
                    else:
                        ver = input("Enter version for " + plugin + ": ")
                        register(plugin, ver, folder)
                    break
                print(plugin)
        if found is True and not forced:
            while choice not in match_list and choice.lower() != "back" and choice.lower() != "reg":
                choice = input('Enter plugin to register (or "back" to search again or "reg"'
                               ' to register search term): ')
            if choice.lower() == "back":
                continue
            else:
                if choice.lower() == "reg":
                    choice = query
                folder = findFolder(choice)
                if folder is None:
                    print("Could not find a folder for " + choice)
                else:
                    ver = input("Enter version for " + choice + ": ")
                    register(choice, ver, folder)
        elif not forced:
            while response != 'y' and response != 'n':
                response = input("Plugin " + query + " not found. Register it anyway? (y/n) ").lower()
            if response == 'y':
                folder = findFolder(query)
                if folder is None:
                    print("Could not find a folder for " + query + ".")
                else:
                    ver = input("Enter version for " + query + ": ")
                    register(query, ver, folder)

# if the github site could not be connected to for some reason, the user must input all their plugins manually
elif not forced:
    print("Plugins must be entered manually.")
    plugin = input("Enter a plugin to register (or \"done\" to stop adding plugins): ")
    while plugin != "done":
        folder = findFolder(plugin)
        if folder is None:
            print("Could not find a folder for " + plugin + ".")
        else:
            ver = input("Enter version: ")
            register(plugin, ver, folder)
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
