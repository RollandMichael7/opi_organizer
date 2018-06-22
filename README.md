# opi_organizer
A python script that converts a flat directory of AreaDetector Control System Studio OPI files into a hierarchical structure, sub-dividing by plugin and version. Aditionally, updates the cross-references of plugin OPIs so that they don't break in the new directory.

If the user has CS Studio installed, the "robust" version of the script also uses the adl2boy feature to convert MEDM adl files into opi files and places them in their appropriate place in the new directory.

**The functions of OPI Organizer have been split into two scripts: convert_and_organize which converts ADL files into OPIs and organzes them, and update_references which replace references to other OPIs with macros which can be used to select which version of a plugin the user wants to link to at runtime.**

A config file can be used to give a path to the local OPI folder, a path to the local Area Detector directory, a path to the CS Studio executable, and a list of plugins (and, if necessary, their versions) to register in the organization.

## Slim ##
Organize Slim only looks at OPI files already put into an OPI folder, automatically converting a "flat" directory into an heirarchial directory. However, if a plugin's name is not in the OPI's name (such as ADBruker's BIS.opi) then the script does not know where to put it unless told by the user.

## Robust ##
Organize Robust searches an entire local Area Detector directory for OPI files, inserting them into the given OPI directory accordingly (in addition to organizing the OPI directory in the same way as Slim). It can also use CS Studio to convert MEDM adl files from the Area Detector directory to create new OPI files and organize them.
