# Given a directory of OPI files created by convert_and_organize, update the OPIs references to other OPIs so that they
# do not break in the new directory structure; uses macros so that the version of a referenced plugin can be chosen at
# runtime.


import os
import re
import fileinput
import sys
from urllib.error import URLError
from urllib.request import urlopen

# example dict of some Area Detector plugins
# dict matches filename substring with plugin name
plugin_dict = {
    # "andor"      : "ADAndor3,
    # "dexela"     : "ADDexela",
    # "eiger"      : "ADEiger",
    # "pilatus"    : "ADPilatus",
    # "prosilica"  : "ADProsilica",
    # "simdetector": "ADSimDetector",
}

# list of filenames that can not be identified as part of a plugin or ADCore, populated by organize()
unidentifiedFiles_dict = {
    # filename : path/to/file
}

plugin_list = []


# given an OPI file directory created by organize(), update its cross-references. The "tag" argument is the identifying
# substring for the plugin "file" belongs to
def cross_reference(opi_dir):
    for root, folders, files in os.walk(opi_dir):
        for file in files:
            if file.endswith(".opi"):
                macro_list = []
                plugin = ""
                tag = ""
                if "ADCore" in os.path.join(root, file):
                    continue
                for p in plugin_dict.keys():
                    if plugin_dict[p] in os.path.join(root, file):
                        if p == "Andor" and "Andor3" in os.path.join(root, file):
                            continue
                        tag = p
                        # print("path: " + os.path.join(root, file))
                        # print("match: " + plugin_dict[p])
                        # print("file: " + file + " tag: " + tag)
                        break
                if tag == "":
                    unidentifiedFiles_dict[file] = os.path.join(root, file)
                    continue
                print("Updating cross references for " + file + "...")
                sys.stderr.write("Editing " + file + ". If the program exits before completion a .bak "
                                                     "backup of the original is created.\n")
                for lineNum, line in enumerate(fileinput.input(os.path.join(root, file), inplace=True)):
                    # search for <opi_file> tag in the OPI
                    if "<opi_file>" in line:
                        path = re.search("<opi_file>(.*)</opi_file>", line)
                        if path is not None:
                            before = ""
                            after = ""
                            path = path.group(1)
                            #if "$" in path:
                            #   continue
                            sys.stderr.write("line " + str(lineNum + 1) + ": " + line)
                            # ignore reference to OPI of the same plugin
                            # (does not need to be changed)
                            if tag.casefold() in path.casefold():
                                if tag == "Andor" and "Andor3" in path:
                                    continue
                                sys.stderr.write("Reference to same plugin left unchanged\n\n")
                                print(line, end="")
                                continue
                            search = re.search("(.*)<opi_file>", line)
                            if search is not None:
                                before = search.group(1)
                            search = re.search("</opi_file>(.*)", line)
                            if search is not None:
                                after = search.group(1)
                            if "AD" in path or "ND" in path or "commonPlugins" in path:
                                plugin = "Core"
                            else:
                                for p in plugin_dict.keys():
                                    if p.casefold() in path.casefold():
                                        if p == "Andor" and "Andor3" in path:
                                            continue
                                        plugin = p
                                        break
                            if plugin != "":
                                line = before + "<opi_file>" + "$(path" + plugin + ")" + os.sep + \
                                       path + "</opi_file>" + after + "\n"
                                if ("path" + plugin) not in macro_list:
                                    macro_list.append("path" + plugin)
                            else:
                                sys.stderr.write("Tag can not be identified; routed to original directory\n\n")
                                line = before + "<opi_file>" + ".." + os.sep + ".." + os.sep + path + "</opi_file>" + after + "\n"
                            sys.stderr.write("converted to: " + line)
                    print(line, end="")
                print("References updated.")
                if len(macro_list) > 0:
                    add_macros(os.path.join(root,file), macro_list)


def add_macros(filePath, macros):
    done = False
    print("Adding macros for " + os.path.basename(filePath) + "...")
    for lineNum, line in enumerate(fileinput.input(filePath, inplace=True)):
        if "<macros>" in line and not done:
            macro_str = ""
            for macro in macros:
                macro_str += "\t<" + macro + ">" + "</" + macro + ">" + "\n"
            line = line + macro_str
            done = True
        print(line, end="")

########################### MAIN ###########################
response = ""
config_path = ""
foundOPI = False
foundAD = False

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
        plugin_list.append(match)
        skip = False
        ver = ""
        if match != "ADCore" and match != "areaDetector":
            skip = False
            if config_path != "":
                for line in open(config_path):
                    if "#" in line:
                        continue
                    if match.casefold() in line.casefold():
                        if "AD" in match:
                            plugin_dict[match[2:]] = match
                        else:
                            plugin_dict[match] = match
                        print("Registered " + match)
                        skip = True
                        break
            if not skip:
                if os.path.isdir(ad_directory + os.sep + match):
                    response = ""
                    while response != 'y' and response != 'n':
                        response = input("Register " + match + "? (y/n) ").lower()
                    if response == 'y':
                        if "AD" in match:
                            plugin_dict[match[2:]] = match
                        else:
                            plugin_dict[match] = match


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
        substr = input("Enter filename substring to search for: ")
        plugin_dict[substr] = plugin
        print(plugin + " added to search, identifying with \"" + substr + "\".")
        plugin = input("Enter plugin to search for (or \"done\" to stop adding plugins): ")

cross_reference(opi_directory)
print("Operation complete.")

# print the path to any unidentified files that were found (and thus left untouched)
if len(unidentifiedFiles_dict) != 0:
    print("Unidentified files:")
    for file in unidentifiedFiles_dict.keys():
        print("\t" + file + " (" + unidentifiedFiles_dict[file] + ")")

quit()
