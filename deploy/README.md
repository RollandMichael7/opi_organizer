# Deployment scripts #
These scripts create a portable deployment of an areaDetector plugin that was previously compiled locally. The script copies all of the
important files from the local installation into a given target directory, and creates an envPaths file that directs the IOC to use the
files in this new directory.

## Requirements ##
- ADSupport, ADCore, and the plugin to be copied must already be compiled already.
- The EPICS modules that these plugins depend on must be compiled already.
  - asyn, autosave, busy, calc, seq, sscan, iocStats
- EPICS base must be compiled already
- The envPaths file uses absolute paths; thus, once the target directory is created it can not be moved. (Unless the envPaths file is changed)

## Usage ##
It is highly reccomended to use the fullDeployment script, which copies the necessary files and can add plugins with the envPaths file fully
configured. Before using any of the scripts, it is necessary to define the BASE, DETECTOR, and EPICS macros which define the path to EPICS base,
areaDetector, and EPICS modules, respectively. The TARGET macro may also be defined in the script, or passed as a command line argument 
(the command line argument has priority over the value in the script). Then simply run the script from bash, and it will search for and copy
the files automatically, and the addPlugin/fullDeployment scripts will prompt for the name of the plugin to add. 
