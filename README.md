# opi_organizer #

**OPI Organizer has been split into several "component" scripts which are called in succession by the run.sh bash script.** Two of the components are convert_and_organize_ad.py and convert_and_organize_epics.py which take directories of either AreaDetector plugins or EPICS modules and extract their ADL files, convert them into OPI files, and put them into a target OPI folder in a heirarchy organized by plugin/module and version. In doing so, these scripts require a path to a CS-Studio executable which can perform this conversion. The third component is update_references.py which takes the files sorted by the other two scripts **(the OPIs *must* be in that organization for this script to work)** and updates their references to other OPIs to function in this new directory structure; in doing this, it uses macros (and default values based on the current directory) such that the version of a linked plugin can be chosen at runtime.

A config file can be used to choose where to put EPICS OPIs, AreaDetector OPIs, where to get AreaDetector plugins from, where to get EPICS modules from, where CS-Studio is located, and which AD Plugins/EPICS modules to use and which versions are being used. **The (relative or absolute) path to the config file can be used as a command line argument to any of the component scripts (including run.sh)** and will be prompted for otherwise.

**For the script to work properly:**
* All AreaDetector plugins must be in the same folder
* All EPICS modules must be in the same folder
* Folders containing modules and plugins must have the **same exact name as the github repo they come from, OR the github repo's name must be a substring of the local folder's name and the module/plugin must be marked in the config file with a version.**
* The folders for the EPICS modules OPIs and the AreaDetector OPIs must be in the same folder
* Update_references.py must be run after/with directories created by the other two components
* The version of CS-Studio being used must support the adl2boy feature; the nightly build of the SNS version is recommended: https://ics-web.sns.ornl.gov/css/products.html

# The "full" versions of the script are old and buggy. Use the run.sh script to run the components which work much better. #
## Slim ##
Organize Slim only looks at OPI files already put into an OPI folder, automatically converting a "flat" directory into an heirarchial directory. However, if a plugin's name is not in the OPI's name (such as ADBruker's BIS.opi) then the script does not know where to put it unless told by the user.

## Robust ##
Organize Robust searches an entire local Area Detector directory for OPI files, inserting them into the given OPI directory accordingly (in addition to organizing the OPI directory in the same way as Slim). It can also use CS Studio to convert MEDM adl files from the Area Detector directory to create new OPI files and organize them.
