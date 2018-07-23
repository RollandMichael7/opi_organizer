# opi_organizer #

OPI organizer is a tool made of several component scripts which, with their powers combined (along with CS Studio), uses a local installation of areaDetector and EPICS modules to create an organized directory of OPI files which use macros in their cross-references to enable version control.

## Requirements ##
- All areaDetector plugins must be in the same folder
- All EPICS modules must be in the same folder
- The names of plugin/module folders must contain the name of the github repo they came from
  - eg. asyn is fine, asyn-4-33 is fine, EPICSasyn is fine, epics-module-1 is not
- Update_references.py must be run after/with directories created by the other two components
- The version of CS-Studio being used must support the adl2boy feature; the nightly build of the SNS version is recommended: https://ics-web.sns.ornl.gov/css/products.html

The overall OPI structure must look something like this for the updated references to work (folder names are arbitrary):

```
-AreaDetector (or some other name)
---R3-3 (or some other name)
-----ADCore (or some other plugin)
-------R3-3 (or some other version)
---------something.opi
        
-Epics (or some other name)
---asyn (or some other module)
-----R4-33 (or some other version)
-------something.opi
```

**The parent folder for AreaDetector OPIs must be on the same level as the target EPICS OPI folder, and the target AreaDetector OPI folder must be one level below the parent AD folder.** The rest of the structure will be created by the script. The config options for this example would be:

```
AD_OPI_DIRECTORY : /home/AreaDetector/R3-3
EPICS_OPI_DIRECTORY : /home/Epics
```

The locations of the actual EPICS modules and AreaDetector plugins have no restrictions.

## Usage ##
It is highly reccomended to use a config file to make running the scripts as painless as possible. An example config file is provided.
The config file specifies:
- Location of areaDetector plugins
- Location of target folder for areaDetector plugin OPIs
- Location of EPICS modules
- Location of target folder for EPICS modules OPIs
- Location of CS Studio executable
- A whitelist of plugins/modules to register in the organization, with the option to indicate their version (otherwise, the script attempts to identify it with git tags or release files)

After creating your config file, simply run the bash script run.sh with the path to the config file as an argument. The script will attempt to identfiy which modules and plugins are present, and attempt to find their version. If the plugin or module is not present in the whitelist, it will ask if you want to register it. Similarly, it will ask for a version if it can not find one. After all plugins/modules are registered, it identifies & converts ADL files using CS Studio, and moves the resulting OPI files into the new structure. It will then fix all the cross-references in the OPIs, replacing them with a macro specific to each plugin/module which can be used to specify a version once several versions are installed. 

**Use the flag -f [path/to/config] to bypass all prompts; any plugins that are not on the whitelist OR whose version can not be identified WILL NOT be reigstered.**

