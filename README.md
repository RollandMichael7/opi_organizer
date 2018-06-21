# opi_organizer
A python script that converts a flat directory of AreaDetector Control System Studio OPI files into a hierarchical structure, sub-dividing by plugin and version. Aditionally, updates the cross-references of plugin OPIs so that they don't break in the new directory.

If the user has CS Studio installed, the "robust" version of the script also uses the adl2boy feature to convert MEDM adl files into opi files and places them in their appropriate place in the new directory.

## Slim ##
Organize slim only looks at OPI files already put into an OPI folder, converting a "flat" directory into an heirarchial directory.

## Robust ##
Organize robust searches the entire Area Detector directory for OPI files, inserting them into the given OPI directory accordingly (in addition to organizing the OPI directory). It can also use CS Studio to convert MEDM adl files from the Area Detector directory to create new OPI files and organize them.
