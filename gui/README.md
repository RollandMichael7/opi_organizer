# Graphic User Interface #
# WARNING: This script is currently only developed and tested on Linux Debian #

For users who prefer a GUI over a command line, this PyQt5 implementation of OPI Organizer
presents a user-friendly visual interface. 

### Requirements ###
- Python 3
- PyQt5
  - On Debian, install with ``` sudo apt-get install python3-pyqt5 ```
  - On Windows, install with ```pip install pyqt5```
- An OPI Organizer config file
  - It is highly reccomended to use ```config``` or ```config_master``` which come in this repository; 
    it is only required to edit the folder paths and CSS path.
- The script **must** be run from this folder in order to correctly call ```run.sh```
    
### Usage ###
Run the script either from an IDE of choice, or from the command line.

Windows:
  - ```py -3.6 organizer.py```

Linux:
  - ```python3 organizer.py```
  
When the script is run, the OPI Organizer main window should pop up. It has fields for the various inputs
required for OPI Organizer to function, however they can not be edited manually. To add input, click the 
"Choose File" button next to the config file field; it will open a file choosing dialog for picking your config
file. The config file will then be used to populate the input fields if possible. If all the input paths are valid,
then the "Run" button will become enabled. Click this button to start the scripts, and then all that's left to do
is wait for the scripts to complete.
