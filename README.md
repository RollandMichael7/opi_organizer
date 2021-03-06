# opi_organizer #

Author: Michael Rolland  
Corresponding Author: Kazimierz Gofron  
Created: June 19, 2018  
Last Updated: June 6, 2019   
Copyright (c): 2018-2019 Brookhaven National Laboratory  

OPI organizer is a tool made of several component scripts which, with their powers combined (along with CS Studio), uses a local installation of areaDetector and EPICS modules to create an organized directory of OPI files which use macros in their cross-references to enable version control.

## Requirements ##
- Python 3 
  - Tested on Windows 10 running 3.6.5 and Debian 9 running 3.5.3
- All areaDetector plugins must be in the same folder
- All EPICS modules must be in the same folder
- The names of plugin/module folders must contain the name of the github repo they came from in order to be detected
  - eg. asyn is fine, asyn-4-33 is fine, EPICSasyn is fine, epics-module-1 is not
- Plugins/modules not obtained from github must be entered manually at runtime or in the config file
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
- Path to CS Studio executable
- A whitelist of plugins/modules to register in the organization, with the option to indicate their version (otherwise, the script attempts to identify it with git tags or release files)
- A blacklist of plugins/modules to ignore
- Additional plugins/modules that are obtained from somewhere other than github

After creating your config file, simply run the bash script run.sh with the path to the config file as an argument. The script will attempt to identfiy which modules and plugins are present, and attempt to find their version. If the plugin or module is not present in the whitelist, it will ask if you want to register it. Similarly, it will ask for a version if it can not find one. After all plugins/modules are registered, it identifies & converts ADL files using CS Studio, and moves the resulting OPI files into the new structure. It will then fix all the cross-references in the OPIs, replacing them with a macro specific to each plugin/module which can be used to specify a version once several versions are installed. 

**Use the flag -f [path/to/config] to bypass all prompts; any plugins that are not on the whitelist OR whose version can not be identified will NOT be reigstered.**

## Using Macros ##
After running the script, all references between OPIs in different folders are replaced by macros which point to whichever version of the target plugin was installed when the script was run. The values of the macros are **paths from the same level as the parent EPICS and AD folders.** These macros have a uniform structure across all areaDetector plugins and EPICS modules, so they can be defined by a parent OPI for version control. For example, to use ADCore R3-2 OPI screens, simply define the ```pathADCore``` macro as 
```
<Parent AD folder name>/<AD version>/ADCore/R3-2

eg.

ADet/R3-3-2/ADCore/R3-2
```
in the main parent OPI screen. Although these will all be defined by default in each individual OPI that needs them, it is reccommended to define them in the main parent screen as well so that version control is easy to track. (Parent macros will override children macros)

**This is the only change the script makes to these OPIs.** Examples from Andor.opi (R2-8):
```
<macros>
    <include_parent_macros>true</include_parent_macros>
</macros>
```
is changed to...
```
<macros>
  <pathADCore>ADet\R3-3\ADCore\R3-3-2</pathADCore>
  <include_parent_macros>true</include_parent_macros>
</macros>
```

<br />
<br />

```
<path>NDFile.opi</path>
```
is changed to...
```
<path>..\..\..\..\$(pathADCore)\NDFile.opi</path>
```
